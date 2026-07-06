"""Build fallback analysis, report text, and model input package."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .utils import (
    CORE_INDICATOR_IMPACTS,
    DATA_FREQUENCY_RULES,
    RATE_CHANGE_IMPLICATIONS,
    RATE_MEANINGS,
    UNAVAILABLE_SOURCES,
    DerivedSignal,
    Metric,
    comparison_rule,
    format_change,
    format_number,
    format_signal_change,
    freshness_label,
    load_intro,
    load_jpy_carry_history_payload,
    load_prompt,
    metric_map,
    now_bjt,
    parse_date_guess,
    rate_label,
)
from .signals import stance_from_score


def _format_signal_value(v: Optional[float], unit: str) -> str:
    if v is None:
        return "N/A"
    if unit == "bp":
        return f"{v:+.1f}bp"
    if unit == "%":
        return f"{v:.2f}%"
    if unit in {"bn", "USD bn"}:
        return f"{v:+,.1f}bn" if v < 0 else f"{v:,.1f}bn"
    if unit == "USD mn/day":
        return f"{v:+,.1f}mn/day"
    if unit in {"ratio", "x"}:
        return f"{v:.2f}x"
    if unit == "pt":
        return f"{v:+.2f}pt"
    if unit in {"index", ""}:
        return f"{v:.2f}"
    return f"{v:.2f}{unit}"


_SIGNAL_BASE_METRICS = {
    "SOFR_ANCHOR": "SOFR",
    "SOFR_VOLUME_IMPACT": "SOFR_VOLUME",
    "BGCR_TGCR": "BGCR",
    "CP_PROXY": "DCPN3M",
    "TGA_FLOW": "TGA",
    "RRP_FLOW": "RRPONTSYD",
    "RRP_BUFFER": "RRPONTSYD",
    "UST_1Y_YIELD": "DGS1",
    "UST_3Y_YIELD": "DGS3",
    "NOMINAL_10Y": "DGS10",
    "REAL_10Y": "DGS10",
    "REAL_10Y_MOMENTUM": "DGS10",
    "HY_CHANGE": "BAMLH0A0HYM2",
    "IG_CHANGE": "BAMLC0A0CM",
    "VIX_RISK": "VIXCLS",
    "VIX_MOMENTUM": "VIXCLS",
    "USD_CHANGE": "DTWEXBGS",
    "UST_10Y2Y": "T10Y2Y",
    "UST_10Y3M": "T10Y3M",
    "NFCI_LEVEL": "NFCI",
    "TBILL_AUCTION_STRESS": "TBILL_AUCTION_SIZE",
    "AUCTION_BTC": "UST_AUCTION_BTC",
}


def _format_signals_table_for_prompt(signals: List[DerivedSignal], metrics: List[Metric]) -> str:
    mm = metric_map(metrics)
    lines = [
        "| 信号ID | 信号名称 | 最新值 | 最新日期 | 上一期值 | 上期日期 | 边际变化 | 频率/口径 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for s in signals:
        vid = s.id or ""
        name = s.name or vid
        base_metric = mm.get(_SIGNAL_BASE_METRICS.get(vid, ""))
        as_of = s.as_of or (base_metric.as_of if base_metric else None) or "NA"
        previous_as_of = (base_metric.previous_as_of if base_metric else None) or "NA"
        frequency = DATA_FREQUENCY_RULES.get(_SIGNAL_BASE_METRICS.get(vid, vid), (base_metric.frequency if base_metric else "派生信号", "", ""))[0]
        value_str = _format_signal_value(s.value, s.unit)
        prev_str = _format_signal_value(s.previous, s.unit) if s.previous is not None else "首期/无上一期"
        change_str = _format_signal_value(s.change, s.unit) if s.change is not None else "首期/无上一期"
        lines.append(f"| {vid} | {name} | {value_str} | {as_of} | {prev_str} | {previous_as_of} | {change_str} | {frequency} |")
    return "\n".join(lines)


def _format_quantity_metrics_table_for_prompt(metrics: List[Metric]) -> str:
    required_ids = ["SOFR_VOLUME", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC"]
    mm = metric_map(metrics)
    lines = [
        "| 指标ID | 最新值 | 上一期值 | 边际变化 | 日期 | 状态 | 解释要求 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    explain = {
        "SOFR_VOLUME": "分析SOFR或SOFR-政策锚时必须引用，用于判断利率偏离作用在多大的回购交易量上。",
        "TBILL_AUCTION_SIZE": "分析短债供给吸收时必须引用，不能只看认购倍数。",
        "TBILL_AUCTION_BTC": "必须与TBILL_AUCTION_SIZE配对解释，判断大规模供给是否被需求承接。",
    }
    for metric_id in required_ids:
        m = mm.get(metric_id)
        if not m:
            lines.append(f"| {metric_id} | 缺失 | 缺失 | 缺失 | NA | missing | {explain[metric_id]}缺失时标记为数据风险。 |")
            continue
        lines.append(
            f"| {metric_id} | {format_number(m.value, m.unit)} | {format_number(m.previous, m.unit)} | "
            f"{format_change(m.change, m.unit)} | {m.as_of or 'NA'} | {freshness_label(m)} | {explain[metric_id]} |"
        )
    return "\n".join(lines)


def _format_upcoming_auctions_table_for_prompt(upcoming_auctions: Optional[Dict[str, Any]]) -> str:
    if not upcoming_auctions or upcoming_auctions.get("status") != "ok":
        return "未来拍卖日程缺失或抓取失败；必须在risk_flags中标为data风险，不得把未知发行量当成零发行。"
    rows = [
        "| 拍卖日 | 结算日 | 类型 | 期限 | 发行规模 | CUSIP |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in upcoming_auctions.get("next_auctions", [])[:12]:
        rows.append(
            f"| {item.get('auctionDate') or 'NA'} | {item.get('issueDate') or 'NA'} | "
            f"{item.get('securityType') or 'NA'} | {item.get('securityTerm') or 'NA'} | "
            f"{item.get('offeringAmountText') or '待公布'} | {item.get('cusip') or 'NA'} |"
        )
    if len(rows) == 2:
        rows.append("| 无未来拍卖 | NA | NA | NA | NA | NA |")
    return "\n".join(rows)


def build_model_input_package(trigger: str, generated: str, stance: str, score: float, metrics: List[Metric], signals: List[DerivedSignal], highlights: List[str], chart_paths: Optional[List[str]] = None, upcoming_auctions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    signals_table = _format_signals_table_for_prompt(signals, metrics)
    quantity_metrics_table = _format_quantity_metrics_table_for_prompt(metrics)
    upcoming_auctions_table = _format_upcoming_auctions_table_for_prompt(upcoming_auctions)
    prompt_text = load_prompt()
    injection = (
        "【衍生信号强制取值表 —— 你必须直接引用下表数值、日期和频率，严禁自行计算或篡改】\n"
        "以下衍生信号已由脚本精确计算完成。写 key_takeaways / risk_flags / evidence 时 MUST 直接使用下表中的「最新值、最新日期、上一期值、上期日期、边际变化、频率/口径」，"
        "不得自行用原始利率相减，不得引用任何与下表不一致的数字；该表只用于模型内部取值，最终输出仍必须是严格 JSON，不得原样输出 Markdown 表。\n\n"
        f"{signals_table}\n\n"
        "【量级指标强制检查表 —— SOFR/T-bill 分析必须引用】\n"
        "如果本次风险涉及SOFR、回购融资或T-bill供给吸收，必须引用下表中的量级指标；"
        "如果表内关键指标缺失，必须在risk_flags中标为data风险，而不是默认为中性。\n\n"
        f"{quantity_metrics_table}\n\n"
        "【未来美债/T-bill拍卖日程 —— 必须纳入供给吸收判断】\n"
        "以下为 TreasuryDirect 当前可查到的未来拍卖安排。分析短债供给、TGA补库、准备金压力时，必须结合未来发行日期和发行规模；"
        "若发行规模待公布，要标为数据风险，不得当作零供给。\n\n"
        f"{upcoming_auctions_table}\n\n"
        "--- 以上表数值为准，以下为分析指令 ---\n\n"
    )
    prompt_text = injection + prompt_text
    return {
        "task": "基于美元流动性介绍文档、结构化市场数据和分析prompt，输出一份可由固定前端模板渲染的结构化 analysis.json。",
        "trigger": trigger or "默认运行",
        "generated_at_bjt": generated,
        "intro_document": load_intro(),
        "analysis_prompt": prompt_text,
        "data": {
            "stance_by_rule_fallback": stance,
            "score_by_rule_fallback": score,
            "highlights_by_rule_fallback": highlights,
            "metrics": [asdict(m) for m in metrics],
            "derived_signals": [asdict(s) for s in signals],
            "quantity_metrics_required": ["SOFR_VOLUME", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC"],
            "quantity_signals_required": ["SOFR_VOLUME_IMPACT", "TBILL_AUCTION_STRESS"],
            "jpy_carry_history": load_jpy_carry_history_payload(),
            "upcoming_auctions": upcoming_auctions or {},
            "data_frequency_rules": DATA_FREQUENCY_RULES,
            "core_indicator_impacts": CORE_INDICATOR_IMPACTS,
            "chart_paths": chart_paths or [],
            "unavailable_sources": UNAVAILABLE_SOURCES,
        },
        "output_contract": {
            "format": "strict_json_only",
            "language": "中文",
            "style": "结论先行、字段稳定、由前端固定模板渲染",
            "forbidden_outputs": ["html", "markdown", "code_fence", "free_text_before_or_after_json"],
            "required_top_level_fields": ["meta", "stance", "key_takeaways", "risk_flags", "narrative_blocks"],
            "marginal_change_rule": "边际变化不能只写数值，必须说明上升/下降对融资压力或流动性的含义。",
            "freshness_evidence_rule": "所有key_takeaways.evidence和risk_flags.evidence必须包含日期、频率/口径、最新值、上一期值或边际变化中的至少三项；重要风险优先五项都写全。",
            "scale_rule": "利率是价格信号，必须结合SOFR_VOLUME、TBILL_AUCTION_SIZE、TBILL_AUCTION_BTC、SOFR_VOLUME_IMPACT、TBILL_AUCTION_STRESS判断价格×规模影响。",
            "required_scale_mentions_rule": "若key_takeaways或risk_flags涉及SOFR/回购融资，文本证据必须包含SOFR_VOLUME或SOFR_VOLUME_IMPACT；若涉及短债供给/拍卖吸收，文本证据必须同时包含TBILL_AUCTION_STRESS、TBILL_AUCTION_SIZE和TBILL_AUCTION_BTC，并结合upcoming_auctions中的未来发行日期和发行规模。",
            "dynamic_sections_rule": "key_takeaways 和 risk_flags 必须根据本次数据动态生成，数量 0-5 条，不固定为 3 条，且两者不得重复表达同一风险。",
            "risk_type_rule": "risk_flags.type 必须区分 market 与 data；数据缺口不能写成真实市场压力。",
            "number_format_rule": "所有输出文本中的数值统一保留两位小数即可；不得输出浮点长尾，例如 -2.9999999999999805bp 应写为 -3.00bp。",
            "rrp_rule": "必须用RRP_FLOW说明边际流量方向，用RRP_BUFFER说明存量缓冲垫厚度；RRP下降短期可释放流动性，但极低RRP_BUFFER代表未来冲击更容易落到准备金。",
            "treasury_yields_rule": "必须在narrative_blocks.treasury_yields中专门分析1Y/3Y/10Y美国国债收益率：1Y=近端政策路径，3Y=中段再定价，10Y=长期折现率锚；10Y必须使用DGS10名义国债收益率，不得用DFII10/TIPS实际收益率替代。",
            "jpy_carry_rule": "JPY Carry 的主目标是判断借日元买美股/美元风险资产的边际资金供给是否顺畅。CFTC 仓位必须做水平+流量（边际）两层分析，且必须拆分多空分项：仅当 CFTC_JPY_GROSS_SHORT 或 CFTC_JPY_SHORT_SHARE 上升（cftc_decomposition.driver=short_building）时，才能下『空头在加仓、carry 资金流支撑美元』的结论；若净空头上升只是多头平仓（long_unwinding/mixed），不得声称 carry 在加杠杆。水平高（short_share 近1年高位）说明未来反转踩踏更剧烈，与当下流量支撑分属不同时间轴。分析顺序：JPY融资成本 -> 美日利差 -> USD/JPY趋势与波动 -> 仓位拥挤度(多空拆解) -> 对美股/风险资产流动性供给的影响。不要把美元流动性收紧对日元的冲击写成主线。", 
            "json_schema_summary": {
                "stance": ["label", "confidence", "score_text", "one_liner"],
                "key_takeaway_item": ["title", "text", "evidence", "related_indicators"],
                "risk_flag_item": ["priority", "severity", "type", "title", "text", "evidence", "related_indicators"],
                "narrative_blocks.treasury_yields": ["label", "one_liner", "analysis"]
            },
        },
    }


def signal_takeaway(signal: DerivedSignal, idx: int) -> Dict[str, Any]:
    value_text = format_number(signal.value, signal.unit)
    previous_text = format_number(signal.previous, signal.unit)
    change_text = format_signal_change(signal.change, signal.unit)
    compare_text = f"当前为 {value_text}，上一期为 {previous_text}，边际变化 {change_text}。"
    titles = {
        "SOFR_ANCHOR": "回购融资相对政策锚的位置",
        "SOFR_VOLUME_IMPACT": "SOFR价格×交易量的资金成本量级",
        "TBILL_AUCTION_STRESS": "T-bill供给×需求吸收压力评分",
        "RRP_FLOW": "RRP边际流量方向",
        "RRP_BUFFER": "RRP存量缓冲垫风险",
        "TGA_FLOW": "财政现金流对准备金的边际影响",
        "CP_PROXY": "企业短融代理利差",
        "UST_10Y2Y": "10年-2年美债曲线",
        "UST_10Y3M": "10年-3个月美债曲线",
        "NFCI_LEVEL": "公开金融条件代理",
    }
    return {
        "title": titles.get(signal.id, f"关键变化 {idx + 1}"),
        "text": f"{signal.name} {compare_text}状态为{signal.severity}。{signal.interpretation}",
        "related_indicators": [signal.id],
    }


def build_fallback_risk_flags(signals: List[DerivedSignal], metrics: List[Metric]) -> List[Dict[str, Any]]:
    priority_order = ["SOFR_ANCHOR", "SOFR_VOLUME_IMPACT", "TGA_FLOW", "RRP_FLOW", "RRP_BUFFER", "TBILL_AUCTION_STRESS", "UST_1Y_YIELD", "UST_3Y_YIELD", "REAL_10Y", "REAL_10Y_MOMENTUM", "HY_CHANGE", "IG_CHANGE", "VIX_RISK", "VIX_MOMENTUM", "USD_CHANGE", "NFCI_LEVEL", "CP_PROXY", "UST_10Y2Y", "UST_10Y3M"]
    priority_index = {signal_id: idx for idx, signal_id in enumerate(priority_order)}
    risky_signals = [s for s in signals if s.severity in {"偏紧", "紧张", "缺失"}]
    risky_signals = sorted(risky_signals, key=lambda s: priority_index.get(s.id, 99))
    flags: List[Dict[str, Any]] = []
    for idx, signal in enumerate(risky_signals[:5]):
        risk_type = "data" if signal.severity == "缺失" else "market"
        severity = "info" if risk_type == "data" else ("high" if idx < 2 else "medium")
        flags.append({
            "priority": "P0" if idx < 2 else ("P1" if idx < 4 else "P2"),
            "severity": severity,
            "type": risk_type,
            "title": signal.name,
            "text": signal.interpretation,
            "evidence": [
                f"最新值：{format_number(signal.value, signal.unit)}",
                f"上一期：{format_number(signal.previous, signal.unit)}",
                f"边际变化：{format_signal_change(signal.change, signal.unit)}",
            ],
            "related_indicators": [signal.id],
        })
    if len(flags) < 5:
        data_gaps = [m for m in metrics if m.status != "ok" or freshness_label(m) == "stale"]
        for metric in data_gaps[: 5 - len(flags)]:
            flags.append({
                "priority": "P2",
                "severity": "info",
                "type": "data",
                "title": f"{rate_label(metric.id)} 数据滞后或降级",
                "text": metric.notes or "该指标本次不能作为最新市场压力判断，只能作为数据风险处理。",
                "evidence": [f"as_of：{metric.as_of or 'NA'}", f"stale_days：{metric.stale_days if metric.stale_days is not None else 'NA'}"],
                "related_indicators": [metric.id],
            })
    return flags[:5]


def build_fallback_analysis(generated: str, context: Dict[str, Any], signals: List[DerivedSignal], highlights: List[str]) -> Dict[str, Any]:
    stance = context.get("stance", "中性")
    metrics = [Metric(**m) for m in context.get("metrics", [])]
    priority = {"SOFR_ANCHOR": 0, "SOFR_VOLUME_IMPACT": 1, "TGA_FLOW": 2, "RRP_FLOW": 3, "RRP_BUFFER": 4, "TBILL_AUCTION_STRESS": 5, "UST_1Y_YIELD": 6, "UST_3Y_YIELD": 7, "REAL_10Y": 8, "REAL_10Y_MOMENTUM": 9, "HY_CHANGE": 10, "IG_CHANGE": 11, "VIX_RISK": 12, "VIX_MOMENTUM": 13, "UST_10Y2Y": 14, "UST_10Y3M": 15, "NFCI_LEVEL": 16, "CP_PROXY": 17}
    selected = sorted(signals, key=lambda s: priority.get(s.id, 99))[:5]
    data_as_of = None
    dates = [m.as_of for m in metrics]
    today = now_bjt().date()
    valid = []
    for raw in dates:
        parsed = parse_date_guess(raw)
        if not parsed:
            continue
        try:
            from datetime import datetime as _dt
            if _dt.fromisoformat(parsed).date() <= today:
                valid.append(parsed)
        except ValueError:
            continue
    data_as_of = max(valid) if valid else None

    return {
        "meta": {
            "generated_at_bjt": generated,
            "data_as_of": data_as_of,
            "model": "rule_summary",
            "input_freshness_note": "脚本自动摘要，模型分析后更新。",
        },
        "stance": {
            "label": stance,
            "score_text": f"规则分数 {context.get('score', 0):.1f}",
            "one_liner": f"今日美元流动性整体判断为{stance}。",
            "confidence": "中等",
        },
        "key_takeaways": [signal_takeaway(signal, idx) for idx, signal in enumerate(selected)],
        "risk_flags": build_fallback_risk_flags(signals, metrics),
        "narrative_blocks": {
            "summary": f"今日美元流动性整体{stance}。",
            "rates": "短端资金利率重点看相对政策锚的位置，尤其是SOFR-IORB；同时用SOFR交易量把价格偏离转化为量级冲击。",
            "balance_sheet": "TGA、RRP与准备金水位决定负债端缓冲空间，RRP需要区分边际方向和存量缓冲垫。",
            "market_transmission": "信用、离岸美元、10年期国债收益率和VIX用于确认压力是否外溢到证券市场。",
            "treasury_yields": {
                "label": "中性",
                "one_liner": "1Y/3Y/10Y收益率组合用于拆分近端政策路径、中段再定价与长期折现率锚。",
                "analysis": "1Y看近端政策路径，3Y看中段再定价，10Y看长期名义折现率锚；正式模型分析会结合三者最新值、边际变化和曲线斜率输出判断。",
            },
        },
    }


def describe_rate_change(metric: Metric) -> str:
    if metric.status != "ok" or metric.value is None:
        return "本次未取到可用数据，不能判断边际变化。"
    if metric.change is None:
        return "缺少上一期可比数据，暂不能判断边际方向。"
    if metric.unit == "%":
        change_value = abs(metric.change * 100.0)
        change_text = f"{change_value:.1f}bp"
    elif metric.unit == "USD bn":
        change_value = abs(metric.change)
        change_text = f"{change_value:.1f}十亿美元"
    elif metric.unit == "ratio":
        change_value = abs(metric.change)
        change_text = f"{change_value:.2f}倍"
    else:
        change_value = abs(metric.change)
        change_text = f"{change_value:.2f}{metric.unit}"
    if change_value < 0.05:
        return "较上一期基本持平，说明边际资金价格没有明显变化。"
    up_text, down_text = RATE_CHANGE_IMPLICATIONS.get(metric.id, ("该指标边际上升，需要结合其他指标判断压力", "该指标边际下降，需要结合其他指标判断宽松程度"))
    if metric.change > 0:
        return f"上升 {change_text}，{up_text}。"
    return f"下降 {change_text}，{down_text}。"


def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(x).replace("\n", " ") for x in row) + " |")
    return "\n".join(out)


def build_report(trigger: str, metrics: List[Metric], signals: List[DerivedSignal], score: float, highlights: List[str], chart_paths: Optional[List[str]] = None, upcoming_auctions: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
    generated = now_bjt().strftime("%Y-%m-%d %H:%M:%S %Z")
    stance = stance_from_score(score)

    metric_rows = []
    for m in metrics:
        metric_rows.append([m.category, m.id, m.name, format_number(m.value, m.unit), format_change(m.change, m.unit), m.as_of or "NA", m.frequency, freshness_label(m)])

    signal_rows = []
    for s in signals:
        signal_rows.append([s.name, format_number(s.value, s.unit), s.severity, s.interpretation])

    unavailable_rows = [[x["name"], x["reason"], x["proxy"]] for x in UNAVAILABLE_SOURCES]
    errors = [m for m in metrics if m.status not in {"ok"}]
    error_lines = [f"- {m.id}: {m.status}; {m.notes}" for m in errors]
    top_highlights = highlights[:5] if highlights else ["未发现明显单点压力，需结合数据新鲜度继续观察。"]

    model_input = build_model_input_package(trigger, generated, stance, score, metrics, signals, highlights, chart_paths, upcoming_auctions)
    context = {
        "trigger": trigger,
        "generated_at_bjt": generated,
        "stance": stance,
        "score": score,
        "metrics": [asdict(m) for m in metrics],
        "derived_signals": [asdict(s) for s in signals],
        "unavailable_sources": UNAVAILABLE_SOURCES,
        "model_prompt": load_prompt(),
        "data_frequency_rules": DATA_FREQUENCY_RULES,
        "core_indicator_impacts": CORE_INDICATOR_IMPACTS,
        "chart_paths": chart_paths or [],
        "upcoming_auctions": upcoming_auctions or {},
        "model_input_schema": "See usd_liquidity_model_input_*.json generated in the same output run.",
    }

    report = f"""# 美元流动性日度简报

生成时间：{generated}
触发语：{trigger or "默认运行"}

## 1. 今日结论

总判断：{stance}

规则分数：{score:.1f}。该分数只用于排序风险，不是投资建议。

关键依据：
"""
    for item in top_highlights:
        report += f"- {item}\n"

    report += "\n## 2. 关键利差和衍生信号\n\n"
    report += markdown_table(["信号", "数值", "状态", "解释"], signal_rows)

    report += "\n\n## 3. 数据指标\n\n"
    report += markdown_table(["模块", "代码", "指标", "最新值", "变化", "日期", "频率", "状态"], metric_rows)

    report += "\n\n## 4. 缺失数据与接口降级\n\n"
    report += markdown_table(["缺失项", "原因", "替代观察"], unavailable_rows)
    if error_lines:
        report += "\n\n" + "\n".join(error_lines)
    else:
        report += "\n\n- 无关键接口错误。"

    return report, context, model_input
