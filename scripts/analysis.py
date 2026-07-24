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
    "UST_1Y_CHANGE_BP": "DGS1",
    "UST_3Y_YIELD": "DGS3",
    "UST_3Y_CHANGE_BP": "DGS3",
    "UST_5Y_YIELD": "DGS5",
    "UST_5Y_CHANGE_BP": "DGS5",
    "UST_7Y_YIELD": "DGS7",
    "UST_7Y_CHANGE_BP": "DGS7",
    "UST_BELLY_MOMENTUM": "DGS7",
    "UST_5Y3Y_SLOPE_BP": "DGS5",
    "UST_7Y5Y_SLOPE_BP": "DGS7",
    "UST_10Y_NOMINAL_LEVEL": "DGS10",
    "UST_10Y_NOMINAL_CHANGE_BP": "DGS10",
    "UST_10Y_REAL_LEVEL": "DFII10",
    "UST_10Y_REAL_CHANGE_BP": "DFII10",
    "NOMINAL_10Y": "DGS10",
    "REAL_10Y": "DFII10",
    "REAL_10Y_MOMENTUM": "DFII10",
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

_TREASURY_CURVE_IDS = {
    "DGS1", "DGS2", "DGS3", "DGS3MO", "DGS5", "DGS7", "DGS10", "T10Y2Y", "T10Y3M",
}

_SOURCE_PRECEDENCE = {
    "Treasury.gov Daily Par Yield Curve": 600,
    "NY Fed Markets API": 550,
    "Treasury FiscalData": 550,
    "TreasuryDirect": 550,
    "OFR STFM": 525,
    "FRED API": 500,
    "FRED CSV": 450,
    "engineered": 400,
    "internal": 100,
}

_JPY_SOURCE_BY_ID = {
    "USDJPY": "BOJ Time-Series Data Search API",
    "JPY_CALL": "BOJ Time-Series Data Search API",
    "JGB10": "MOF history + CNBC latest patch",
    "US_JP_10Y": "engineered from DGS10 and JGB10",
    "CFTC_JPY_NET_OI": "CFTC Public Reporting API",
    "CFTC_JPY_GROSS_SHORT": "CFTC Public Reporting API",
    "CFTC_JPY_GROSS_LONG": "CFTC Public Reporting API",
    "CFTC_JPY_SHORT_SHARE": "CFTC Public Reporting API",
    "CFTC_JPY_OPEN_INTEREST": "CFTC Public Reporting API",
    "USDJPY_VOL20": "engineered from USDJPY",
}


def _source_rank(metric: Metric) -> int:
    rank = _SOURCE_PRECEDENCE.get(metric.source, 300)
    if metric.id.upper() in _TREASURY_CURVE_IDS and metric.source == "Treasury.gov Daily Par Yield Curve":
        return 700
    return rank


def _metric_selection_key(metric: Metric) -> Tuple[int, str, int, int]:
    usable = int(metric.status == "ok" and metric.value is not None)
    as_of = parse_date_guess(metric.as_of) or ""
    has_previous = int(metric.previous is not None)
    return usable, as_of, _source_rank(metric), has_previous


def _canonical_metric_fact(metric: Metric, candidates: List[Metric]) -> Dict[str, Any]:
    alternatives = [
        {
            "source": candidate.source,
            "as_of": candidate.as_of,
            "status": candidate.status,
        }
        for candidate in candidates
        if candidate is not metric
    ]
    reason = (
        "按可用状态、最新有效日期、显式来源优先级、上一期可比值完整性依次选择；"
        f"本次选中 {metric.source}（as_of={metric.as_of or 'NA'}）。"
    )
    return {
        "fact_id": f"metric:{metric.id.upper()}",
        "id": metric.id.upper(),
        "name": metric.name,
        "category": metric.category,
        "value": metric.value,
        "previous": metric.previous,
        "change": metric.change,
        "unit": metric.unit,
        "as_of": metric.as_of,
        "previous_as_of": metric.previous_as_of,
        "frequency": metric.frequency,
        "source": metric.source,
        "source_url": metric.source_url,
        "status": metric.status,
        "stale_days": metric.stale_days,
        "notes": metric.notes,
        "source_selection": {
            "selected_source": metric.source,
            "precedence_rank": _source_rank(metric),
            "reason": reason,
            "alternatives": alternatives,
        },
    }


def _build_canonical_metrics(metrics: List[Metric]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    grouped: Dict[str, List[Metric]] = {}
    for metric in metrics:
        grouped.setdefault(metric.id.upper(), []).append(metric)

    facts: List[Dict[str, Any]] = []
    quality_flags: List[Dict[str, Any]] = []
    for metric_id in sorted(grouped):
        candidates = grouped[metric_id]
        selected = max(candidates, key=_metric_selection_key)
        facts.append(_canonical_metric_fact(selected, candidates))
        if len(candidates) > 1:
            quality_flags.append({
                "fact_id": f"quality:duplicate_metric:{metric_id}",
                "type": "source_selection",
                "severity": "info",
                "metric_id": metric_id,
                "message": f"{metric_id} 有 {len(candidates)} 个来源；模型仅使用 canonical 选中行。",
                "selected_source": selected.source,
                "discarded_sources": [m.source for m in candidates if m is not selected],
            })
        if selected.status != "ok" or selected.value is None:
            quality_flags.append({
                "fact_id": f"quality:missing_metric:{metric_id}",
                "type": "missing",
                "severity": "warning",
                "metric_id": metric_id,
                "message": selected.notes or "canonical 指标缺失或接口降级。",
            })
        elif freshness_label(selected) == "stale":
            quality_flags.append({
                "fact_id": f"quality:stale_metric:{metric_id}",
                "type": "stale",
                "severity": "warning",
                "metric_id": metric_id,
                "as_of": selected.as_of,
                "stale_days": selected.stale_days,
                "message": "canonical 指标已陈旧，只能作为背景或数据风险。",
            })
    return facts, quality_flags


def _build_derived_facts(signals: List[DerivedSignal], metrics: List[Metric]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    mm = metric_map(metrics)
    grouped: Dict[str, List[DerivedSignal]] = {}
    for signal in signals:
        grouped.setdefault(signal.id.upper(), []).append(signal)

    facts: List[Dict[str, Any]] = []
    quality_flags: List[Dict[str, Any]] = []
    for signal_id in sorted(grouped):
        candidates = grouped[signal_id]
        selected = max(candidates, key=lambda item: (int(item.value is not None), parse_date_guess(item.as_of) or "", int(item.previous is not None)))
        base_metric_id = _SIGNAL_BASE_METRICS.get(signal_id)
        base_metric = mm.get(base_metric_id or "")
        facts.append({
            "fact_id": f"derived:{signal_id}",
            "id": signal_id,
            "name": selected.name,
            "value": selected.value,
            "previous": selected.previous,
            "change": selected.change,
            "unit": selected.unit,
            "severity": selected.severity,
            "interpretation": selected.interpretation,
            "as_of": selected.as_of or (base_metric.as_of if base_metric else None),
            "previous_as_of": base_metric.previous_as_of if base_metric else None,
            "frequency": DATA_FREQUENCY_RULES.get(base_metric_id or signal_id, (base_metric.frequency if base_metric else "derived", "", ""))[0],
            "base_fact_ids": [f"metric:{base_metric_id}"] if base_metric_id else [],
        })
        if len(candidates) > 1:
            quality_flags.append({
                "fact_id": f"quality:duplicate_derived:{signal_id}",
                "type": "deduplicated",
                "severity": "info",
                "signal_id": signal_id,
                "message": f"{signal_id} 出现重复衍生信号；模型仅使用最新且完整的一条。",
            })
    return facts, quality_flags


def _normalized_jpy_points(points: Any) -> List[Tuple[str, float]]:
    rows: List[Tuple[str, float]] = []
    if not isinstance(points, list):
        return rows
    for point in points:
        if not isinstance(point, dict):
            continue
        as_of = parse_date_guess(point.get("date"))
        value = point.get("value")
        if as_of and isinstance(value, (int, float)):
            rows.append((as_of, float(value)))
    return sorted(rows, key=lambda row: row[0])


def _jpy_change(rows: List[Tuple[str, float]], days: int) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    if not rows:
        return None, None, None
    latest_date = parse_date_guess(rows[-1][0])
    if not latest_date:
        return None, None, None
    from datetime import date, timedelta
    cutoff = (date.fromisoformat(latest_date) - timedelta(days=days)).isoformat()
    previous = None
    for row in rows:
        if row[0] <= cutoff:
            previous = row
        else:
            break
    if previous is None:
        return None, None, None
    change = rows[-1][1] - previous[1]
    pct_change = (change / previous[1] * 100.0) if previous[1] else None
    return change, pct_change, previous[0]


def _compact_jpy_carry_payload() -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
    payload = load_jpy_carry_history_payload()
    quality_flags: List[Dict[str, Any]] = []
    if not payload or not isinstance(payload.get("jpy_carry"), dict):
        quality_flags.append({
            "fact_id": "quality:jpy_carry_missing",
            "type": "missing",
            "severity": "warning",
            "message": "JPY carry 数据缺失；不得把缺失解释为中性。",
        })
        return None, quality_flags

    jpy = payload["jpy_carry"]
    history = jpy.get("history") if isinstance(jpy.get("history"), dict) else {}
    cards = {card.get("id"): card for card in jpy.get("cards", []) if isinstance(card, dict) and card.get("id")}
    indicator_facts: List[Dict[str, Any]] = []
    for indicator_id in sorted(history):
        rows = _normalized_jpy_points(history.get(indicator_id))
        if not rows:
            quality_flags.append({
                "fact_id": f"quality:jpy_missing:{indicator_id}",
                "type": "missing",
                "severity": "warning",
                "metric_id": indicator_id,
                "message": "JPY carry 指标无可用观测。",
            })
            continue
        change_1d, change_1d_pct, compare_1d = _jpy_change(rows, 1)
        change_5d, change_5d_pct, compare_5d = _jpy_change(rows, 5)
        change_20d, change_20d_pct, compare_20d = _jpy_change(rows, 20)
        latest_value = rows[-1][1]
        percentile = sum(1 for _, value in rows if value <= latest_value) / len(rows)
        card = cards.get(indicator_id, {})
        indicator_facts.append({
            "fact_id": f"jpy:{indicator_id}",
            "id": indicator_id,
            "name": card.get("label") or indicator_id,
            "value": latest_value,
            "as_of": rows[-1][0],
            "change_1d": change_1d,
            "change_1d_pct": change_1d_pct,
            "comparison_as_of_1d": compare_1d,
            "change_5d": change_5d,
            "change_5d_pct": change_5d_pct,
            "comparison_as_of_5d": compare_5d,
            "change_20d": change_20d,
            "change_20d_pct": change_20d_pct,
            "comparison_as_of_20d": compare_20d,
            "history_percentile": percentile,
            "history_observations": len(rows),
            "source": _JPY_SOURCE_BY_ID.get(indicator_id, "see jpy_carry sources"),
            "interpretation_note": card.get("why"),
        })

    decomposition = jpy.get("cftc_decomposition") if isinstance(jpy.get("cftc_decomposition"), dict) else {}
    compact = {
        "meta": jpy.get("meta", {}),
        "indicators": indicator_facts,
        "cftc_decomposition": {
            "fact_id": "jpy:CFTC_DECOMPOSITION",
            "driver": decomposition.get("driver", "unknown"),
            "text": decomposition.get("text", ""),
            "gross_short_change": decomposition.get("gross_short_change"),
            "gross_long_change": decomposition.get("gross_long_change"),
            "short_share_change": decomposition.get("short_share_change"),
            "net_change": decomposition.get("net_change"),
            "carry_usd_support": decomposition.get("carry_usd_support", False),
        },
        "sources": jpy.get("sources", []),
        "notes": jpy.get("notes", []),
    }
    return compact, quality_flags


def _build_event_facts(upcoming_auctions: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    quality_flags: List[Dict[str, Any]] = []
    if not upcoming_auctions or upcoming_auctions.get("status") != "ok":
        quality_flags.append({
            "fact_id": "quality:upcoming_auctions_missing",
            "type": "missing",
            "severity": "warning",
            "message": "未来拍卖日程缺失或抓取失败；未知发行量不得视为零。",
        })
        return {"upcoming_auctions": [], "gross_totals": [], "status": "missing"}, quality_flags

    auctions = upcoming_auctions.get("auctions") or upcoming_auctions.get("next_auctions") or []
    compact_auctions: List[Dict[str, Any]] = []
    totals: Dict[Tuple[str, str, str], float] = {}
    totals_by_auction_date: Dict[str, float] = {}
    totals_by_issue_date: Dict[str, float] = {}
    totals_by_security_type: Dict[str, float] = {}
    for index, item in enumerate(auctions):
        if not isinstance(item, dict):
            continue
        auction_date = item.get("auctionDate") or "NA"
        issue_date = item.get("issueDate") or "NA"
        security_type = item.get("securityType") or "NA"
        security_term = item.get("securityTerm") or "NA"
        amount = item.get("offeringAmount")
        amount_value = float(amount) if isinstance(amount, (int, float)) else None
        fact_id = f"event:auction:{auction_date}:{security_type}:{security_term}:{item.get('cusip') or index}"
        compact_auctions.append({
            "fact_id": fact_id,
            "event_type": "treasury_auction_announcement",
            "auction_date": auction_date,
            "issue_date": issue_date,
            "security_type": security_type,
            "security_term": security_term,
            "cusip": item.get("cusip") or "",
            "gross_announced_offering_usd_bn": amount_value,
            "maturities_usd_bn": None,
            "net_cash_impact_usd_bn": None,
            "reserve_impact": "unknown_without_settlement_maturities_tga_and_funding_confirmation",
            "source": "TreasuryDirect",
        })
        if amount_value is None:
            quality_flags.append({
                "fact_id": f"quality:auction_amount_missing:{auction_date}:{security_type}:{security_term}:{index}",
                "type": "missing",
                "severity": "warning",
                "event_fact_id": fact_id,
                "message": "未来拍卖 offeringAmount 待公布，不得按零计。",
            })
        else:
            key = (auction_date, issue_date, security_type)
            totals[key] = totals.get(key, 0.0) + amount_value
            totals_by_auction_date[auction_date] = totals_by_auction_date.get(auction_date, 0.0) + amount_value
            totals_by_issue_date[issue_date] = totals_by_issue_date.get(issue_date, 0.0) + amount_value
            totals_by_security_type[security_type] = totals_by_security_type.get(security_type, 0.0) + amount_value

    gross_totals = [
        {
            "fact_id": f"event:gross_total:{auction_date}:{issue_date}:{security_type}",
            "auction_date": auction_date,
            "issue_date": issue_date,
            "security_type": security_type,
            "gross_announced_offering_usd_bn": amount,
            "maturities_usd_bn": None,
            "net_cash_impact_usd_bn": None,
            "reserve_impact": "unknown_without_settlement_maturities_tga_and_funding_confirmation",
        }
        for (auction_date, issue_date, security_type), amount in sorted(totals.items())
    ]
    gross_totals_by_auction_date = [
        {
            "fact_id": f"event:gross_total_by_auction_date:{auction_date}",
            "auction_date": auction_date,
            "gross_announced_offering_usd_bn": amount,
            "maturities_usd_bn": None,
            "net_cash_impact_usd_bn": None,
            "reserve_impact": "unknown_without_settlement_maturities_tga_and_funding_confirmation",
        }
        for auction_date, amount in sorted(totals_by_auction_date.items())
    ]
    gross_totals_by_issue_date = [
        {
            "fact_id": f"event:gross_total_by_issue_date:{issue_date}",
            "issue_date": issue_date,
            "gross_announced_offering_usd_bn": amount,
            "maturities_usd_bn": None,
            "net_cash_impact_usd_bn": None,
            "reserve_impact": "unknown_without_settlement_maturities_tga_and_funding_confirmation",
        }
        for issue_date, amount in sorted(totals_by_issue_date.items())
    ]
    gross_totals_by_security_type = [
        {
            "fact_id": f"event:gross_total_by_security_type:{security_type}",
            "security_type": security_type,
            "gross_announced_offering_usd_bn": amount,
            "maturities_usd_bn": None,
            "net_cash_impact_usd_bn": None,
            "reserve_impact": "unknown_without_settlement_maturities_tga_and_funding_confirmation",
        }
        for security_type, amount in sorted(totals_by_security_type.items())
    ]
    gross_total_announced = sum(totals_by_auction_date.values()) if totals_by_auction_date else None
    return {
        "status": "ok",
        "as_of": upcoming_auctions.get("as_of"),
        "source_url": upcoming_auctions.get("source_url"),
        "upcoming_auctions": compact_auctions,
        "gross_totals": gross_totals,
        "gross_totals_by_auction_date": gross_totals_by_auction_date,
        "gross_totals_by_issue_date": gross_totals_by_issue_date,
        "gross_totals_by_security_type": gross_totals_by_security_type,
        "gross_total_announced": {
            "fact_id": "event:gross_total_announced",
            "gross_announced_offering_usd_bn": gross_total_announced,
            "maturities_usd_bn": None,
            "net_cash_impact_usd_bn": None,
            "reserve_impact": "unknown_without_settlement_maturities_tga_and_funding_confirmation",
        },
        "gross_not_net_rule": "offeringAmount 仅为已公告毛发行；maturities/net_cash_impact/reserve_impact 在缺少结算、到期、TGA和融资确认时保持未知。",
    }, quality_flags


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


def build_model_input_package(trigger: str, generated: str, metrics: List[Metric], signals: List[DerivedSignal], upcoming_auctions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    canonical_metrics, metric_quality = _build_canonical_metrics(metrics)
    derived_facts, signal_quality = _build_derived_facts(signals, metrics)
    event_facts, event_quality = _build_event_facts(upcoming_auctions)
    jpy_carry, jpy_quality = _compact_jpy_carry_payload()
    quality_flags = metric_quality + signal_quality + event_quality + jpy_quality
    prompt_text = (
        "【本次模型事实包硬约束】\n"
        "只能使用 data.facts 中的 canonical_metrics、derived_facts、event_facts、jpy_carry 与 quality_flags；"
        "每个 metric ID 已去重，禁止回到来源列表自行二选一，禁止使用旧报告、fallback stance/score/highlights 或图表路径锚定结论。\n"
        "必须按资金价格、流动性数量与缓冲、美债供给与资产定价、跨市场传导与杠杆四轴独立判断后再合成 stance。"
        "P0 market 必须是已实现压力，至少引用两个独立且新鲜的 fact_id 交叉确认；其中融资压力 P0 至少包含一个核心资金价格事实及一个同层或下游确认。"
        "低 RRP 单独只能是 P1 结构脆弱性；未来拍卖 offeringAmount 是 gross announced issuance，不是净融资或确定性准备金消耗。\n"
        "每条 key_takeaway/risk_flag 必须给出 claim_type、跨两数组唯一的 dedupe_key、以及只指向本次事实包的 fact_ids；key_takeaways 只允许 observed，inference/scenario 只进入 risk_flags。\n\n"
        + load_prompt()
    )
    return {
        "task": "基于唯一、可追溯的 canonical facts，完成四轴美元流动性分析并输出固定前端可渲染的严格 analysis.json。",
        "trigger": trigger or "默认运行",
        "generated_at_bjt": generated,
        "intro_document": load_intro(),
        "analysis_prompt": prompt_text,
        "data": {
            "facts": {
                "canonical_metrics": canonical_metrics,
                "derived_facts": derived_facts,
                "event_facts": event_facts,
                "jpy_carry": jpy_carry,
                "quality_flags": quality_flags,
                "source_selection_policy": {
                    "dedupe_key": "upper(metric.id)",
                    "selection_order": ["usable status/value", "latest as_of", "explicit source precedence", "previous-value completeness"],
                    "treasury_curve_precedence": ["Treasury.gov Daily Par Yield Curve", "FRED API", "FRED CSV"],
                    "rule": "snapshot/SQLite 可保留多来源；模型事实包每个 metric ID 只暴露一个 canonical row，并记录选中原因与备选来源。",
                },
            },
            "required_fact_ids": {
                "quantity_metrics": ["metric:SOFR_VOLUME", "metric:TBILL_AUCTION_SIZE", "metric:TBILL_AUCTION_BTC"],
                "quantity_signals": ["derived:SOFR_VOLUME_IMPACT", "derived:TBILL_AUCTION_STRESS"],
                "treasury_belly": ["metric:DGS1", "metric:DGS3", "metric:DGS5", "metric:DGS7"],
            },
            "data_frequency_rules": DATA_FREQUENCY_RULES,
            "core_indicator_impacts": CORE_INDICATOR_IMPACTS,
            "unavailable_sources": UNAVAILABLE_SOURCES,
        },
        "output_contract": {
            "format": "strict_json_only",
            "language": "中文",
            "style": "结论先行、事实可追溯、字段稳定、由前端固定模板渲染",
            "forbidden_outputs": ["html", "markdown", "code_fence", "free_text_before_or_after_json"],
            "required_top_level_fields": ["meta", "stance", "axis_assessment", "key_takeaways", "risk_flags", "narrative_blocks"],
            "fact_scope_rule": "只能使用data.facts中的canonical_metrics、derived_facts、event_facts、jpy_carry、quality_flags；禁止使用旧报告、fallback结论、图表路径或模型自行重算值。",
            "canonical_metrics_rule": "每个metric ID只能引用唯一canonical row；source_selection记录选中来源、优先级、原因和备选来源。",
            "four_axis_rule": "先独立评估四轴：funding_price资金价格、liquidity_buffer数量与缓冲、treasury_pricing美债供给与资产定价、cross_market_transmission跨市场传导与杠杆；再综合形成stance，不得用单一总分替代。",
            "p0_confirmation_rule": "P0 market仅用于已实现压力，至少两个独立且新鲜的fact_id交叉确认；融资压力P0必须含一个核心资金价格事实和一个同层或下游确认。低RRP、未来gross拍卖或单一情景不得单独列P0。",
            "claim_rule": "每条key_takeaway和risk_flag必须包含claim_type、跨两个数组唯一的dedupe_key、非空fact_ids；fact_ids必须存在于本次facts。key_takeaways只允许observed；inference和scenario只能进入risk_flags，scenario必须有非空condition。",
            "marginal_change_rule": "边际变化不能只写数值，必须说明上升/下降对融资压力、流动性或资产定价的含义。",
            "freshness_evidence_rule": "所有key_takeaways.evidence和risk_flags.evidence必须包含日期、频率/口径、最新值、上一期值或边际变化中的至少三项；P0引用的事实必须新鲜。",
            "scale_rule": "利率是价格信号，必须结合SOFR_VOLUME、TBILL_AUCTION_SIZE、TBILL_AUCTION_BTC、SOFR_VOLUME_IMPACT、TBILL_AUCTION_STRESS判断价格×规模影响。",
            "required_scale_mentions_rule": "若涉及SOFR/回购融资，fact_ids必须包含metric:SOFR_VOLUME或derived:SOFR_VOLUME_IMPACT；若涉及已完成T-bill拍卖吸收，必须同时引用derived:TBILL_AUCTION_STRESS、metric:TBILL_AUCTION_SIZE和metric:TBILL_AUCTION_BTC。",
            "gross_auction_rule": "event_facts中的offeringAmount与gross totals仅为已公告毛发行，不等于净融资、净现金筹集或确定性准备金消耗；maturities/net_cash_impact缺失时必须保持未知。所有合计直接引用gross_totals_by_auction_date、gross_totals_by_issue_date、gross_totals_by_security_type或gross_total_announced，禁止手工求和。只有结算/到期净额、TGA变化、准备金或资金价格等事实确认后，才可把供给写成已实现流动性冲击；否则只能写scenario。",
            "dynamic_sections_rule": "key_takeaways和risk_flags各0-5条，动态生成；两数组dedupe_key全局唯一，不得重复同一风险。",
            "risk_type_rule": "risk_flags.type必须区分market与data；数据缺口不能写成真实市场压力。",
            "number_format_rule": "所有输出文本中的数值统一保留两位小数；不得输出浮点长尾。",
            "rrp_rule": "必须用RRP_FLOW说明边际流量方向，用RRP_BUFFER说明存量缓冲垫厚度；RRP下降短期可释放流动性，但极低RRP_BUFFER仅代表结构脆弱性，单独最高为P1。",
            "treasury_yields_rule": "国债收益率主框架固定为1Y/3Y/5Y/7Y：1Y近端政策路径、3Y中段再定价、5Y/7Y腹部传导。四个期限都必须拆成水平+边际变化，并直接引用canonical/derived facts；腹部斜率使用脚本预计算事实。10Y仅作曲线/长期名义折现率背景，不替代1Y/3Y/5Y/7Y。",
            "jpy_carry_rule": "JPY Carry按融资成本、美日利差、USD/JPY趋势与波动、CFTC多空拆解、风险资产传导分析。只有cftc_decomposition.driver为short_building或two_sided_building_short_dominant时，才能称空头主导加仓并边际支撑美元；long_unwinding、two_sided_building_long_dominant、two_sided_reduction、mixed或unknown均不得声称carry在加杠杆。水平拥挤与当下流量必须分开。",
            "json_schema_summary": {
                "stance": ["label", "confidence", "score_text", "one_liner"],
                "axis_item": ["label", "summary", "fact_ids"],
                "key_takeaway_item": ["title", "text", "evidence", "related_indicators", "claim_type", "dedupe_key", "fact_ids"],
                "risk_flag_item": ["priority", "severity", "type", "title", "text", "evidence", "related_indicators", "claim_type", "dedupe_key", "fact_ids"],
                "narrative_blocks.treasury_yields": ["label", "one_liner", "analysis"],
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
        "evidence": [
            f"最新值：{value_text}",
            f"上一期：{previous_text}",
            f"边际变化：{change_text}",
        ],
        "related_indicators": [signal.id],
        "claim_type": "observed",
        "dedupe_key": f"derived:{signal.id.lower()}",
        "fact_ids": [f"derived:{signal.id.upper()}"],
    }


def build_fallback_risk_flags(signals: List[DerivedSignal], metrics: List[Metric]) -> List[Dict[str, Any]]:
    priority_order = ["SOFR_ANCHOR", "SOFR_VOLUME_IMPACT", "TGA_FLOW", "RRP_FLOW", "RRP_BUFFER", "TBILL_AUCTION_STRESS", "UST_1Y_YIELD", "UST_3Y_YIELD", "UST_5Y_YIELD", "UST_7Y_YIELD", "HY_CHANGE", "IG_CHANGE", "VIX_RISK", "VIX_MOMENTUM", "USD_CHANGE", "NFCI_LEVEL", "CP_PROXY", "UST_10Y2Y", "UST_10Y3M", "NOMINAL_10Y", "REAL_10Y", "REAL_10Y_MOMENTUM"]
    priority_index = {signal_id: idx for idx, signal_id in enumerate(priority_order)}
    risky_signals = [s for s in signals if s.severity in {"偏紧", "紧张", "缺失"}]
    risky_signals = sorted(risky_signals, key=lambda s: priority_index.get(s.id, 99))
    flags: List[Dict[str, Any]] = []
    for idx, signal in enumerate(risky_signals[:5]):
        risk_type = "data" if signal.severity == "缺失" else "market"
        severity = "info" if risk_type == "data" else ("high" if idx < 2 else "medium")
        flags.append({
            "priority": "P1" if idx < 4 else "P2",
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
            "claim_type": "observed",
            "dedupe_key": f"risk:derived:{signal.id.lower()}",
            "fact_ids": [f"derived:{signal.id.upper()}"],
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
                "claim_type": "observed",
                "dedupe_key": f"risk:data:{metric.id.lower()}",
                "fact_ids": [f"metric:{metric.id.upper()}"],
            })
    return flags[:5]


def _fallback_axis_assessment(signals: List[DerivedSignal]) -> Dict[str, Any]:
    axis_signal_ids = {
        "funding_price": {"SOFR_ANCHOR", "SOFR_VOLUME_IMPACT", "BGCR_TGCR", "CP_PROXY"},
        "liquidity_buffer": {"TGA_FLOW", "RRP_FLOW", "RRP_BUFFER"},
        "treasury_pricing": {"TBILL_AUCTION_STRESS", "UST_1Y_YIELD", "UST_3Y_YIELD", "UST_5Y_YIELD", "UST_7Y_YIELD"},
        "cross_market_transmission": {"HY_CHANGE", "IG_CHANGE", "VIX_RISK", "VIX_MOMENTUM", "USD_CHANGE", "NFCI_LEVEL"},
    }
    labels = {"紧张": 4, "偏紧": 3, "中性": 2, "偏松": 1, "缺失": 0}
    result: Dict[str, Any] = {}
    for axis, ids in axis_signal_ids.items():
        selected = [signal for signal in signals if signal.id in ids]
        selected.sort(key=lambda signal: labels.get(signal.severity, 2), reverse=True)
        lead = selected[0] if selected else None
        result[axis] = {
            "label": lead.severity if lead else "数据不足",
            "summary": lead.interpretation if lead else "规则摘要缺少足够事实，等待模型复核。",
            "fact_ids": [f"derived:{signal.id.upper()}" for signal in selected[:4]],
        }
    return result


def build_fallback_analysis(generated: str, context: Dict[str, Any], signals: List[DerivedSignal], highlights: List[str]) -> Dict[str, Any]:
    stance = context.get("stance", "中性")
    metrics = [Metric(**m) for m in context.get("metrics", [])]
    priority = {"SOFR_ANCHOR": 0, "SOFR_VOLUME_IMPACT": 1, "TGA_FLOW": 2, "RRP_FLOW": 3, "RRP_BUFFER": 4, "TBILL_AUCTION_STRESS": 5, "UST_1Y_YIELD": 6, "UST_3Y_YIELD": 7, "UST_5Y_YIELD": 8, "UST_7Y_YIELD": 9, "HY_CHANGE": 10, "IG_CHANGE": 11, "VIX_RISK": 12, "VIX_MOMENTUM": 13, "UST_10Y2Y": 14, "UST_10Y3M": 15, "NOMINAL_10Y": 16, "REAL_10Y": 17, "REAL_10Y_MOMENTUM": 18, "NFCI_LEVEL": 19, "CP_PROXY": 20}
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
    takeaways = [signal_takeaway(signal, idx) for idx, signal in enumerate(selected)]
    takeaway_fact_ids = {fact_id for item in takeaways for fact_id in item.get("fact_ids", [])}
    risk_flags = [
        item for item in build_fallback_risk_flags(signals, metrics)
        if not takeaway_fact_ids.intersection(item.get("fact_ids", []))
    ]

    return {
        "meta": {
            "generated_at_bjt": generated,
            "data_as_of": data_as_of,
            "model": "rule_summary",
            "input_freshness_note": "脚本自动摘要，模型分析后更新。",
        },
        "stance": {
            "label": stance,
            "score_text": "规则摘要仅供兜底展示；正式结论须由四轴事实综合形成。",
            "one_liner": f"今日美元流动性规则摘要为{stance}，等待模型按四轴事实复核。",
            "confidence": "低",
        },
        "axis_assessment": _fallback_axis_assessment(signals),
        "key_takeaways": takeaways,
        "risk_flags": risk_flags,
        "narrative_blocks": {
            "summary": f"今日美元流动性整体{stance}。",
            "rates": "短端资金利率重点看相对政策锚的位置，尤其是SOFR-IORB；同时用SOFR交易量把价格偏离转化为量级冲击。",
            "balance_sheet": "TGA、RRP与准备金水位决定负债端缓冲空间，RRP需要区分边际方向和存量缓冲垫。",
            "market_transmission": "信用、离岸美元、10年期国债收益率和VIX用于确认压力是否外溢到证券市场。",
            "treasury_yields": {
                "label": "中性",
                "one_liner": "1Y/3Y/5Y/7Y腹部组合用于拆分近端政策路径、中段再定价与腹部传导，10Y仅作折现率背景。",
                "analysis": "1Y看近端政策路径，3Y看中段再定价，5Y/7Y看腹部传导，10Y仅作长期名义折现率背景；正式模型分析会结合1Y/3Y/5Y/7Y最新值、边际变化和腹部斜率输出判断，10Y斜率用于衰退/降息预期观察。",
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

    mm = metric_map(metrics)
    rate_rows = []
    for metric_id in ("EFFR", "SOFR", "IORB", "OBFR", "TGCR", "BGCR", "DGS1", "DGS3", "DGS5", "DGS7", "DGS10", "DFII10"):
        metric = mm.get(metric_id)
        if not metric:
            continue
        rate_rows.append([
            rate_label(metric.id),
            RATE_MEANINGS.get(metric.id, metric.name),
            describe_rate_change(metric),
        ])

    signal_rows = []
    for s in signals:
        signal_rows.append([s.name, format_number(s.value, s.unit), s.severity, s.interpretation])

    unavailable_rows = [[x["name"], x["reason"], x["proxy"]] for x in UNAVAILABLE_SOURCES]
    errors = [m for m in metrics if m.status not in {"ok"}]
    error_lines = [f"- {m.id}: {m.status}; {m.notes}" for m in errors]
    top_highlights = highlights[:5] if highlights else ["未发现明显单点压力，需结合数据新鲜度继续观察。"]

    model_input = build_model_input_package(trigger, generated, metrics, signals, upcoming_auctions)
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

    report += "\n## 2. 利率表\n\n"
    report += markdown_table(["利率", "含义", "边际变化"], rate_rows)

    report += "\n\n## 3. 关键利差和衍生信号\n\n"
    report += markdown_table(["信号", "数值", "状态", "解释"], signal_rows)

    report += "\n\n## 4. 数据指标\n\n"
    report += markdown_table(["模块", "代码", "指标", "最新值", "变化", "日期", "频率", "状态"], metric_rows)

    report += "\n\n## 5. 缺失数据与接口降级\n\n"
    report += markdown_table(["缺失项", "原因", "替代观察"], unavailable_rows)
    if error_lines:
        report += "\n\n" + "\n".join(error_lines)
    else:
        report += "\n\n- 无关键接口错误。"

    return report, context, model_input
