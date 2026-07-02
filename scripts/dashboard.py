"""Dashboard data building, charts payload, and transmission chain."""

from __future__ import annotations

import math
import os
import sqlite3
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from .utils import (
    CORE_INDICATOR_IMPACTS,
    DATA_FREQUENCY_RULES,
    RATE_MEANINGS,
    UNAVAILABLE_SOURCES,
    DerivedSignal,
    Metric,
    change_direction,
    chart_points,
    comparison_rule,
    format_change,
    format_number,
    format_signal_change,
    freshness_label,
    importance_for,
    load_jpy_carry_history_payload,
    metric_map,
    now_bjt,
    parse_date_guess,
    rate_label,
    trim_series,
)
from .charts import fetch_fred_series_points
from .fetchers import fetch_cftc_jpy_position


def latest_nonfuture_date(dates: List[Optional[str]]) -> Optional[str]:
    today = now_bjt().date()
    valid: List[str] = []
    for raw in dates:
        parsed = parse_date_guess(raw)
        if not parsed:
            continue
        try:
            if datetime.fromisoformat(parsed).date() <= today:
                valid.append(parsed)
        except ValueError:
            continue
    return max(valid) if valid else None


def latest_point(rows: List[Tuple[str, float]], offset: int = 0) -> Optional[Tuple[str, float]]:
    if not rows or len(rows) <= offset:
        return None
    return rows[-1 - offset]


def first_point_before(rows: List[Tuple[str, float]], latest_date: str, lookback_days: int) -> Optional[Tuple[str, float]]:
    try:
        threshold = datetime.fromisoformat(latest_date).date() - timedelta(days=lookback_days)
    except Exception:
        return rows[0] if rows else None
    candidates = [(date, value) for date, value in rows if parse_date_guess(date) and datetime.fromisoformat(parse_date_guess(date)).date() <= threshold]
    return candidates[-1] if candidates else (rows[0] if rows else None)


def pct_change(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    if current is None or previous is None or previous == 0:
        return None
    return (current / previous - 1.0) * 100.0


def realized_vol_from_series(rows: List[Tuple[str, float]], window: int = 20) -> Optional[float]:
    points = [value for _, value in rows[-(window + 1):] if value and value > 0]
    if len(points) < 6:
        return None
    returns = [math.log(points[i] / points[i - 1]) for i in range(1, len(points))]
    if len(returns) < 2:
        return None
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    return math.sqrt(variance) * math.sqrt(252) * 100.0


def build_charts_payload(series_bundle: Dict[str, List[Tuple[str, float]]], upcoming_auctions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    sofr_anchor_label = "SOFR-IORB（担保隔夜融资利率-准备金余额利率）" if series_bundle.get("IORB") else "SOFR-Policy Anchor（担保隔夜融资利率-政策锚）"
    specs = [
        ("short_rates_7d", "短端资金利率：最近一周", 10, "%", [("EFFR", "EFFR（有效联邦基金利率）"), ("SOFR", "SOFR（担保隔夜融资利率）"), ("TGCR", "TGCR（三方一般抵押品利率）"), ("BGCR", "BGCR（广义一般抵押品利率）")]),
        ("short_rates_30d", "短端资金利率：最近一月", 35, "%", [("EFFR", "EFFR（有效联邦基金利率）"), ("SOFR", "SOFR（担保隔夜融资利率）"), ("TGCR", "TGCR（三方一般抵押品利率）"), ("BGCR", "BGCR（广义一般抵押品利率）")]),
        ("anchor_spreads_7d", "关键利差：最近一周", 10, "bp", [("SOFR_ANCHOR", sofr_anchor_label), ("BGCR_TGCR", "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）")]),
        ("anchor_spreads_30d", "关键利差：最近一月", 35, "bp", [("SOFR_ANCHOR", sofr_anchor_label), ("BGCR_TGCR", "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）")]),
        ("sofr_volume_30d", "SOFR交易量：最近一月", 35, "USD bn", [("SOFR_VOLUME", "SOFR Volume（SOFR交易量）")]),
        ("tbill_auction_size_45d", "T-bill拍卖规模：最近45日", 45, "USD bn", [("TBILL_AUCTION_SIZE", "T-bill Auction Size（短期国债拍卖规模）")]),
        ("tbill_auction_btc_45d", "T-bill拍卖认购倍数：最近45日", 45, "ratio", [("TBILL_AUCTION_BTC", "T-bill Auction BTC（短期国债拍卖投标覆盖倍数）")]),
        ("cp_proxy_30d", "企业短融代理利差：最近一月", 35, "bp", [("CP_PROXY", "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）")]),
        ("credit_oas_30d", "信用利差：最近一月", 35, "%", [("BAMLH0A0HYM2", "HY OAS（高收益债期权调整利差）"), ("BAMLC0A0CM", "IG OAS（投资级公司债期权调整利差）")]),
        ("treasury_yields_30d", "美国国债收益率：1Y / 3Y / 10Y 最近一月", 35, "%", [("DGS1", "1Y Treasury Yield（1年期美国国债收益率）"), ("DGS3", "3Y Treasury Yield（3年期美国国债收益率）"), ("DGS10", "10Y Treasury Yield（10年期美国国债收益率）")]),
        ("real_yields_30d", "真实贴现率：最近一月", 35, "%", [("DFII10", "10Y Real Yield（10年期TIPS实际收益率）")]),
        ("treasury_curve_30d", "美债长短端利差：最近一月", 35, "%", [("T10Y2Y", "10Y-2Y Treasury Spread（10年-2年美债利差）"), ("T10Y3M", "10Y-3M Treasury Spread（10年-3个月美债利差）")]),
        ("risk_appetite_30d", "证券市场风险偏好：最近一月", 35, "index", [("VIXCLS", "VIX（标普500隐含波动率指数）")]),
        ("financial_conditions_30d", "公开金融条件代理：最近一月", 35, "index", [("NFCI", "NFCI（芝加哥联储全国金融条件指数）")]),
        ("fed_liability_30d", "Fed负债端水位：最近一月", 35, "USD bn", [("TGA", "TGA（财政部一般账户）", "y"), ("RRP", "RRP（隔夜逆回购）", "y1")]),
    ]
    charts = []
    for chart_id, title, days, unit, ids in specs:
        series = []
        for item in ids:
            series_id, label = item[0], item[1]
            y_axis = item[2] if len(item) >= 3 else "y"
            points = chart_points(series_bundle.get(series_id, []), days)
            if points:
                series.append({"id": series_id, "label": label, "points": points, "y_axis": y_axis})
        chart_payload = {"id": chart_id, "title": title, "chart_type": "line", "unit": unit, "series": series}
        if any(s.get("y_axis") == "y1" for s in series):
            chart_payload["dual_axis"] = True
            chart_payload["y_axes"] = {"y": "TGA（十亿美元）", "y1": "RRP（十亿美元）"}
        charts.append(chart_payload)
    
    # 新增：合并美债发行量图表（前20日+未来10日）
    combined_supply_chart = build_combined_treasury_supply_chart(series_bundle, upcoming_auctions)
    if combined_supply_chart:
        charts.append(combined_supply_chart)
    
    return {"charts": charts}


def build_upcoming_auction_charts(upcoming_auctions: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not upcoming_auctions or upcoming_auctions.get("status") != "ok":
        return []
    bill_points = []
    for day in upcoming_auctions.get("bill_schedule", []):
        if not isinstance(day, dict):
            continue
        date = day.get("auctionDate")
        value = day.get("totalBillOffering")
        if date and value is not None:
            bill_points.append({"date": date, "value": value})
    total_by_date: Dict[str, float] = {}
    for item in upcoming_auctions.get("auctions", []):
        if not isinstance(item, dict):
            continue
        date = item.get("auctionDate")
        value = item.get("offeringAmount")
        if date and value is not None:
            total_by_date[date] = total_by_date.get(date, 0.0) + float(value)
    total_points = [{"date": date, "value": total_by_date[date]} for date in sorted(total_by_date)]
    series = []
    if bill_points:
        series.append({"id": "UPCOMING_TBILL_SUPPLY", "label": "Upcoming T-bill Supply（未来短债发行规模）", "points": bill_points, "y_axis": "y"})
    if total_points:
        series.append({"id": "UPCOMING_TOTAL_TREASURY_SUPPLY", "label": "Upcoming Total Treasury Supply（未来已公告美债发行总额）", "points": total_points, "y_axis": "y"})
    if not series:
        return []
    return [{
        "id": "upcoming_tbill_supply_60d",
        "title": "未来已公告拍卖规模：T-bill / Total",
        "chart_type": "line",
        "unit": "USD bn",
        "series": series,
        "data_source": "dashboard_data.upcoming_auctions.bill_schedule / auctions",
        "note": "只包含TreasuryDirect已公告发行规模；未公告规模不当作零供给。",
    }]


def build_combined_treasury_supply_chart(
    series_bundle: Dict[str, List[Tuple[str, float]]],
    upcoming_auctions: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Build total Treasury issuance chart from landed engineered series."""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
    if not os.path.exists(db_path):
        return None

    today = now_bjt().date()
    start = (today - timedelta(days=20)).isoformat()
    end = (today + timedelta(days=10)).isoformat()
    snapshot_file = f"engineered_treasury_supply_{today.isoformat()}.json"
    ingested_at = now_bjt().strftime("%Y-%m-%d %H:%M:%S UTC+08:00")

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS engineered_series_ts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id       TEXT    NOT NULL,
            series_name     TEXT,
            category        TEXT,
            as_of           TEXT    NOT NULL,
            value           REAL,
            unit            TEXT,
            source          TEXT,
            source_url      TEXT,
            snapshot_file   TEXT    NOT NULL,
            ingested_at     TEXT    NOT NULL,
            notes           TEXT,
            UNIQUE(series_id, as_of)
        )
        ''')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_engineered_series_id_date ON engineered_series_ts(series_id, as_of)')

        cur.execute(
            """
            SELECT auction_date, SUM(offering_amount_bn) AS total_amount
            FROM treasury_auctions_ts
            WHERE id IN (
                SELECT MAX(id)
                FROM treasury_auctions_ts
                WHERE auction_date >= ?
                  AND auction_date <= ?
                  AND offering_amount_bn IS NOT NULL
                GROUP BY auction_date, COALESCE(cusip, ''), COALESCE(security_type, ''), COALESCE(security_term, '')
            )
            GROUP BY auction_date
            ORDER BY auction_date
            """,
            (start, end)
        )
        computed_rows = [(row[0], row[1]) for row in cur.fetchall() if row[1] is not None]
        for date, value in computed_rows:
            cur.execute(
                '''INSERT INTO engineered_series_ts
                    (series_id, series_name, category, as_of, value, unit, source, source_url, snapshot_file, ingested_at, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(series_id, as_of) DO UPDATE SET
                       value=excluded.value,
                       ingested_at=excluded.ingested_at,
                       notes=excluded.notes''',
                (
                    "TREASURY_COMBINED_SUPPLY",
                    "Total Treasury Supply",
                    "treasury_supply",
                    date,
                    value,
                    "USD bn",
                    "engineered_from_treasury_auctions_ts",
                    "",
                    snapshot_file,
                    ingested_at,
                    "Aggregates all Treasury security types by auction date; window previous 20 days + next 10 days",
                )
            )
        conn.commit()
        cur.execute(
            """SELECT as_of, value FROM engineered_series_ts
               WHERE series_id = ? AND snapshot_file = ?
               ORDER BY as_of""",
            ("TREASURY_COMBINED_SUPPLY", snapshot_file)
        )
        points = [{"date": row[0], "value": row[1]} for row in cur.fetchall() if row[1] is not None]
    finally:
        conn.close()

    if not points:
        return None

    return {
        "id": "treasury_combined_supply_30d",
        "title": "合并美债发行量：前20日 + 后10日",
        "chart_type": "line",
        "unit": "USD bn",
        "series": [
            {
                "id": "TREASURY_COMBINED_SUPPLY",
                "label": "Total Treasury Supply（全部美债发行量）",
                "points": points,
                "y_axis": "y"
            }
        ],
        "data_source": "SQLite engineered_series_ts.TREASURY_COMBINED_SUPPLY（由 treasury_auctions_ts 工程聚合后落表）",
        "note": "统计所有类型美债的当日发行规模；未公告规模不当作零。该图专用窗口：前20日 + 后10日。",
    }


def build_indicator_card(metric: Metric) -> Dict[str, Any]:
    update_rule, data_lag, compare_rule = DATA_FREQUENCY_RULES.get(metric.id, (metric.frequency, "以接口返回日期为准", comparison_rule(metric)))
    return {
        "id": metric.id,
        "label": rate_label(metric.id),
        "category": metric.category,
        "value": metric.value,
        "value_text": format_number(metric.value, metric.unit),
        "unit": metric.unit,
        "previous": metric.previous,
        "change": metric.change,
        "change_text": format_change(metric.change, metric.unit),
        "change_direction": change_direction(metric.change, metric.unit),
        "as_of": metric.as_of,
        "previous_as_of": metric.previous_as_of,
        "meaning": RATE_MEANINGS.get(metric.id, metric.name),
        "frequency": update_rule,
        "data_lag": data_lag,
        "comparison_basis": compare_rule,
        "freshness": freshness_label(metric),
        "importance": importance_for(metric.id),
        "interpretation_hint": "",
        "source": metric.source,
        "source_url": metric.source_url,
        "status": metric.status,
        "notes": metric.notes,
    }


def group_indicators(metrics: List[Metric]) -> List[Dict[str, Any]]:
    group_defs = [
        ("front_end_rates", "短端资金利率", "观察银行间与回购市场资金价格是否偏离政策锚。", ["EFFR", "SOFR", "OBFR", "TGCR", "BGCR", "IORB", "POLICY_UPPER_NYFED"]),
        ("fed_liability", "Fed负债端水位", "观察TGA、RRP、SOMA与准备金水位对银行体系流动性的影响。", ["TGA", "RRPONTSYD", "SOMA", "WRESBAL"]),
        ("treasury_curve", "国债收益率与曲线", "观察1Y、3Y、10Y收益率组合、真实折现率和曲线利差的变化。", ["DGS1", "DGS3", "DGS10", "DFII10", "DGS30", "T10Y2Y", "T10Y3M", "DTB3", "DGS3MO", "DGS2"]),
        ("collateral_treasury", "抵押品与国债吸收", "观察SOFR交易量、T-bill拍卖量级/认购倍数、回购抵押品链条和交割压力。", ["SOFR_VOLUME", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC", "UST_AUCTION_BTC", "REPO_FAILS_UST"]),
        ("offshore_credit", "离岸美元、信用与金融条件", "观察压力是否外溢到离岸美元、信用市场和综合金融条件。", ["DTWEXBGS", "DCPN3M", "BAMLC0A0CM", "BAMLH0A0HYM2", "NFCI"]),
        ("securities_risk", "证券市场风险偏好", "观察利率和信用条件是否进一步反映到股票波动率和风险偏好。", ["VIXCLS"]),
    ]
    cards = [build_indicator_card(metric) for metric in metrics]
    by_id = {card["id"]: card for card in cards}
    groups = []
    for group_id, title, description, ids in group_defs:
        indicators = [by_id[indicator_id] for indicator_id in ids if indicator_id in by_id]
        if indicators:
            groups.append({"id": group_id, "title": title, "description": description, "indicators": indicators})
    return groups


def build_trading_dashboard(metrics: List[Metric], signals: List[DerivedSignal]) -> Dict[str, Any]:
    mm = metric_map(metrics)
    sm = {s.id: s for s in signals}

    signal_base_metrics = {
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

    def signal_item(signal_id: str, priority: str, why: str) -> Optional[Dict[str, Any]]:
        signal = sm.get(signal_id)
        if not signal:
            return None
        # 从底层metric获取时间信息，或使用signal自带的时间
        base_metric_id = signal_base_metrics.get(signal_id)
        base_metric = mm.get(base_metric_id) if base_metric_id else None
        as_of = signal.as_of if hasattr(signal, 'as_of') and signal.as_of else base_metric.as_of if base_metric else None
        freq_info = DATA_FREQUENCY_RULES.get(base_metric_id or signal_id, (base_metric.frequency if base_metric else "", "", ""))
        return {
            "type": "signal",
            "id": signal.id,
            "label": signal.name,
            "priority": priority,
            "value_text": format_number(signal.value, signal.unit),
            "previous_text": format_number(signal.previous, signal.unit),
            "change_text": format_signal_change(signal.change, signal.unit),
            "severity": signal.severity,
            "why": why,
            "interpretation": signal.interpretation,
            "as_of": as_of,
            "frequency": freq_info[0] if freq_info[0] else "派生信号",
        }

    def metric_item(metric_id: str, priority: str, why: str) -> Optional[Dict[str, Any]]:
        metric = mm.get(metric_id)
        if not metric:
            return None
        return {
            "type": "metric",
            "id": metric.id,
            "label": rate_label(metric.id),
            "priority": priority,
            "value_text": format_number(metric.value, metric.unit),
            "previous_text": format_number(metric.previous, metric.unit),
            "change_text": format_change(metric.change, metric.unit),
            "severity": "缺失" if metric.status != "ok" else "中性",
            "why": why,
            "interpretation": RATE_MEANINGS.get(metric.id, metric.name),
            "as_of": metric.as_of,
            "frequency": DATA_FREQUENCY_RULES.get(metric.id, (metric.frequency, "", ""))[0],
        }

    def compact(items: List[Optional[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        return [item for item in items if item]

    return {
        "core": compact([
            signal_item("SOFR_ANCHOR", "P0", "回购融资是否高于政策锚"),
            signal_item("SOFR_VOLUME_IMPACT", "P0", "SOFR价格偏离作用在多大交易量上"),
            metric_item("TGA", "P0", "财政抽水/放水"),
            signal_item("RRP_FLOW", "P0", "RRP边际流量方向"),
            signal_item("RRP_BUFFER", "P0", "非银现金缓冲垫厚度"),
            metric_item("WRESBAL", "P1", "银行准备金水位"),
            signal_item("UST_1Y_YIELD", "P1", "短债近端政策路径"),
            signal_item("UST_3Y_YIELD", "P1", "中段政策路径再定价"),
            signal_item("REAL_10Y", "P1", "10年期国债收益率压力"),
            signal_item("HY_CHANGE", "P1", "信用压力是否扩散"),
        ]),
        "confirm": compact([
            metric_item("OBFR", "P2", "银行融资压力是否扩散"),
            metric_item("TGCR", "P2", "三方回购融资确认"),
            metric_item("BGCR", "P2", "广义回购融资确认"),
            signal_item("BGCR_TGCR", "P2", "回购内部结构扰动"),
            signal_item("REAL_10Y_MOMENTUM", "P2", "10年期国债收益率边际变化"),
            signal_item("IG_CHANGE", "P2", "投资级信用融资"),
            signal_item("VIX_RISK", "P2", "证券市场波动率水平"),
            signal_item("VIX_MOMENTUM", "P2", "证券市场风险偏好边际变化"),
            metric_item("SOFR_VOLUME", "P2", "回购融资交易量级"),
            signal_item("TBILL_AUCTION_STRESS", "P2", "T-bill供给×需求吸收压力"),
            metric_item("TBILL_AUCTION_BTC", "P2", "短债拍卖需求强度"),
            metric_item("UST_AUCTION_BTC", "P2", "国债供给吸收能力"),
            metric_item("REPO_FAILS_UST", "P2", "抵押品交割链条"),
            metric_item("DTWEXBGS", "P2", "离岸美元压力"),
            signal_item("CP_PROXY", "P2", "企业短融压力代理"),
        ]),
        "background": compact([
            metric_item("SOMA", "B", "QT结构背景"),
            metric_item("DGS1", "B", "近端政策路径"),
            metric_item("DGS30", "B", "长期期限溢价"),
            signal_item("UST_10Y2Y", "B", "收益率曲线斜率"),
            signal_item("UST_10Y3M", "B", "衰退/降息预期"),
            signal_item("NFCI_LEVEL", "B", "公开金融条件代理"),
        ]),
        "core_chart_ids": ["anchor_spreads_30d", "fed_liability_30d", "treasury_combined_supply_30d", "us_jp_spread", "treasury_yields_30d", "jpy_usdjpy_funding_1y"],
        "chart_groups": [
            {"id": "core_monthly", "title": "核心图表", "description": "最近一月核心视图：资金利差、Fed负债端、美债发行、利差、收益率与JPY carry。", "chart_ids": ["anchor_spreads_30d", "fed_liability_30d", "treasury_combined_supply_30d", "us_jp_spread", "treasury_yields_30d", "jpy_usdjpy_funding_1y"], "default_open": True},
            {"id": "review_background", "title": "背景复盘", "description": "复盘时再看，不占用日常交易主视图。", "chart_ids": ["short_rates_30d", "sofr_volume_30d", "real_yields_30d", "treasury_curve_30d", "cp_proxy_30d", "credit_oas_30d", "risk_appetite_30d", "financial_conditions_30d", "tbill_auction_size_45d", "tbill_auction_btc_45d", "upcoming_tbill_supply_60d", "jpy_jgb_curve_1y", "jpy_cftc_position_2y", "jpy_effective_fx_3y"], "default_open": False},
        ],
    }


def build_jpy_carry_overlay(metrics: List[Metric], signals: List[DerivedSignal]) -> Dict[str, Any]:
    history_payload = load_jpy_carry_history_payload()
    if history_payload and isinstance(history_payload.get("jpy_carry"), dict):
        jpy_carry = history_payload["jpy_carry"]
        if history_payload.get("charts") and isinstance(jpy_carry, dict):
            jpy_carry.setdefault("chart_ids", [chart.get("id") for chart in history_payload.get("charts", []) if chart.get("id")])
        return jpy_carry

    mm = metric_map(metrics)
    rows_usdjpy: List[Tuple[str, float]] = []
    rows_jgb10: List[Tuple[str, float]] = []
    rows_jpy_3m: List[Tuple[str, float]] = []
    errors: List[str] = []

    try:
        rows_usdjpy = fetch_fred_series_points("DEXJPUS", 90, "index")
    except Exception as exc:
        errors.append(f"DEXJPUS unavailable: {exc}")
    try:
        rows_jgb10 = fetch_fred_series_points("IRLTLT01JPM156N", 520, "%")
    except Exception as exc:
        errors.append(f"JGB10 proxy unavailable: {exc}")
    try:
        rows_jpy_3m = fetch_fred_series_points("IR3TIB01JPM156N", 520, "%")
    except Exception as exc:
        errors.append(f"JPY 3M funding proxy unavailable: {exc}")

    usdjpy_latest = latest_point(rows_usdjpy)
    usdjpy_5d_base = first_point_before(rows_usdjpy, usdjpy_latest[0], 5) if usdjpy_latest else None
    usdjpy_20d_base = first_point_before(rows_usdjpy, usdjpy_latest[0], 20) if usdjpy_latest else None
    usdjpy_5d = pct_change(usdjpy_latest[1], usdjpy_5d_base[1]) if usdjpy_latest and usdjpy_5d_base else None
    usdjpy_20d = pct_change(usdjpy_latest[1], usdjpy_20d_base[1]) if usdjpy_latest and usdjpy_20d_base else None
    usdjpy_vol = realized_vol_from_series(rows_usdjpy, 20)

    us10y = mm.get("DGS10")
    us2y = mm.get("DGS2")
    vix = mm.get("VIXCLS")
    hy = mm.get("BAMLH0A0HYM2")
    jgb10_latest = latest_point(rows_jgb10)
    jgb10_prev = latest_point(rows_jgb10, 1)
    jpy3m_latest = latest_point(rows_jpy_3m)
    cftc = fetch_cftc_jpy_position()

    us_jp_10y_spread = (us10y.value - jgb10_latest[1]) * 100.0 if us10y and us10y.value is not None and jgb10_latest else None
    us_jp_10y_prev = (us10y.previous - jgb10_prev[1]) * 100.0 if us10y and us10y.previous is not None and jgb10_prev else None
    us_jp_10y_change = (us_jp_10y_spread - us_jp_10y_prev) if us_jp_10y_spread is not None and us_jp_10y_prev is not None else None
    us_jp_short_spread = (us2y.value - jpy3m_latest[1]) * 100.0 if us2y and us2y.value is not None and jpy3m_latest else None

    score = 0.0
    reasons: List[str] = []
    if usdjpy_5d is not None:
        if usdjpy_5d <= -2.0:
            score += 2.0
            reasons.append(f"USD/JPY 5日下跌 {usdjpy_5d:.1f}%，日元快速升值，carry 平仓压力上升。")
        elif usdjpy_5d <= -1.0:
            score += 1.0
            reasons.append(f"USD/JPY 5日下跌 {usdjpy_5d:.1f}%，需要警惕日元空头回补。")
        elif usdjpy_5d >= 1.0:
            score -= 0.5
            reasons.append(f"USD/JPY 5日上涨 {usdjpy_5d:.1f}%，趋势仍支持 carry 延续。")
    if usdjpy_vol is not None:
        if usdjpy_vol >= 16.0:
            score += 2.0
            reasons.append(f"USD/JPY 20日实现波动率约 {usdjpy_vol:.1f}%，汇率波动已进入高风险区。")
        elif usdjpy_vol >= 12.0:
            score += 1.0
            reasons.append(f"USD/JPY 20日实现波动率约 {usdjpy_vol:.1f}%，波动上升会削弱 carry 风险收益。")
    if vix and vix.value is not None:
        if vix.value >= 25.0:
            score += 2.0
            reasons.append(f"VIX {vix.value:.2f}，全球风险偏好恶化，carry 去杠杆风险高。")
        elif vix.value >= 20.0:
            score += 1.0
            reasons.append(f"VIX {vix.value:.2f}，风险偏好边际转弱。")
        elif vix.value <= 17.0:
            score -= 0.5
            reasons.append(f"VIX {vix.value:.2f}，风险偏好尚可，暂未触发系统性去杠杆。")
    if us_jp_10y_change is not None and us_jp_10y_change <= -25.0:
        score += 1.0
        reasons.append(f"美日10年利差较上一期收窄 {abs(us_jp_10y_change):.0f}bp，carry 收益端吸引力下降。")
    if cftc.get("crowded_ratio") is not None and cftc["crowded_ratio"] < -0.25:
        score += 1.0
        reasons.append(f"CFTC日元投机净头寸/未平仓合约约 {cftc['crowded_ratio']:.1%}，日元空头拥挤，若汇率反转会放大回补。")
    if hy and hy.value is not None and hy.value >= 4.0:
        score += 1.0
        reasons.append(f"HY OAS {hy.value:.2f}%，信用压力上升会提高跨资产去杠杆概率。")

    score = max(0.0, min(6.0, score))
    if score >= 4.0:
        label = "偏高"
    elif score >= 2.0:
        label = "中性偏高"
    else:
        label = "中性"
    if not reasons:
        reasons.append("关键触发器未形成共振：汇率、波动率、VIX与信用利差暂未同时指向 carry unwind。")

    def card(card_id: str, label_text: str, value_text: str, change_text: str, why: str, as_of: Optional[str]) -> Dict[str, Any]:
        return {"id": card_id, "label": label_text, "value_text": value_text, "change_text": change_text, "why": why, "as_of": as_of or "NA"}

    cards = [
        card("USDJPY", "USD/JPY（日元兑美元）", f"{usdjpy_latest[1]:.2f}" if usdjpy_latest else "NA", f"5日 {usdjpy_5d:+.1f}% / 20日 {usdjpy_20d:+.1f}%" if usdjpy_5d is not None and usdjpy_20d is not None else "NA", "快速下跌代表日元升值和空头回补压力；缓慢上行通常支持 carry 延续。", usdjpy_latest[0] if usdjpy_latest else None),
        card("USDJPY_VOL", "USD/JPY 20日实现波动率", f"{usdjpy_vol:.1f}%" if usdjpy_vol is not None else "NA", "波动越高，carry 夏普越差", "carry trade 最怕汇率波动突然放大，尤其是日元升值伴随波动抬升。", usdjpy_latest[0] if usdjpy_latest else None),
        card("US_JP_10Y_SPREAD", "美日10Y利差", f"{us_jp_10y_spread:.0f}bp" if us_jp_10y_spread is not None else "NA", format_signal_change(us_jp_10y_change, "bp"), "长端利差代表收益端吸引力；快速收窄会削弱海外持债和 carry 激励。", min(us10y.as_of, jgb10_latest[0]) if us10y and us10y.as_of and jgb10_latest else None),
        card("US_JP_SHORT_SPREAD", "美日短端利差代理", f"{us_jp_short_spread:.0f}bp" if us_jp_short_spread is not None else "NA", "JPY 3M为月频代理", "短端利差越宽，融资日元买美元资产的收益激励越强；收窄则提高平仓风险。", min(us2y.as_of, jpy3m_latest[0]) if us2y and us2y.as_of and jpy3m_latest else None),
        card("CFTC_JPY", "CFTC日元投机净头寸", f"{cftc['value']:,.0f}" if cftc.get("value") is not None else "NA", f"变化 {cftc['change']:,.0f}" if cftc.get("change") is not None else cftc.get("status", "NA"), "负值代表投机资金净做空日元；越拥挤，遇到日元升值时越容易踩踏回补。", cftc.get("as_of")),
        card("GLOBAL_RISK", "全球风险偏好确认", f"VIX {vix.value:.2f}" if vix and vix.value is not None else "NA", f"HY OAS {hy.value:.2f}%" if hy and hy.value is not None else "HY OAS NA", "VIX和信用利差同步上行时，carry trade 更容易从收益策略变成融资回补风险。", vix.as_of if vix else None),
    ]

    sources = [
        {"name": "FRED / Federal Reserve", "items": ["DEXJPUS USD/JPY", "DGS2/DGS10 美债收益率", "VIXCLS", "HY OAS"]},
        {"name": "OECD via FRED", "items": ["IRLTLT01JPM156N 日本10年国债收益率（月频）", "IR3TIB01JPM156N 日本3个月利率代理（月频）"]},
        {"name": "CFTC Public Reporting", "items": ["JPY futures non-commercial net positions，周频背景"]},
        {"name": "缺口", "items": ["FX options implied vol", "risk reversal", "true cross-currency basis 通常为商业数据，当前未接入"]},
    ]
    if errors or cftc.get("status") != "ok":
        sources.append({"name": "本次降级", "items": errors + ([f"CFTC: {cftc.get('notes')}"] if cftc.get("status") != "ok" else [])})

    return {
        "meta": {"lookback": "USD/JPY 90天；JGB/JPY短端代理约520天；CFTC周频最新2期", "note": "日元 carry 风险不是只看 USD/JPY，必须结合利差、波动、仓位和全球风险偏好。"},
        "risk": {"label": label, "score": round(score, 1), "reasons": reasons[:5]},
        "cards": cards,
        "sources": sources,
    }


def build_transmission_chain(context: Dict[str, Any], signals: List[DerivedSignal]) -> Dict[str, Any]:
    metrics_dict = {str(m.get("id", "")).upper(): m for m in context.get("metrics", []) if isinstance(m, dict)}
    signal_map = {s.id: s for s in signals}

    def signal_status(signal_ids: List[str], metric_ids: Optional[List[str]] = None) -> str:
        selected = [signal_map.get(sid) for sid in signal_ids if signal_map.get(sid)]
        if any(s.severity in {"紧张", "偏紧"} for s in selected):
            return "偏紧"
        if any(s.severity == "缺失" for s in selected):
            return "数据缺口"
        if any(s.severity == "偏松" for s in selected):
            return "偏松"
        if metric_ids and any((metrics_dict.get(mid) or {}).get("status") not in {None, "ok"} for mid in metric_ids):
            return "数据缺口"
        return "中性"

    def problem_type(status: str) -> str:
        if status == "数据缺口":
            return "data"
        if status in {"偏紧", "紧张"}:
            return "market"
        return "none"

    def metric_value_text(m: Optional[Dict[str, Any]]) -> str:
        if not m:
            return "NA"
        return format_number(m.get("value"), m.get("unit", ""))

    def signal_value_text(s: Optional[DerivedSignal]) -> str:
        if not s:
            return "NA"
        return format_number(s.value, s.unit)

    def node(node_id: str, label: str, role: str, status: str, evidence: List[str], diagnosis: str) -> Dict[str, Any]:
        ptype = problem_type(status)
        return {"id": node_id, "label": label, "role": role, "status": status, "is_problem_area": ptype != "none", "problem_type": ptype, "evidence": evidence, "diagnosis": diagnosis}

    tga = metrics_dict.get("TGA")
    rrp = metrics_dict.get("RRPONTSYD")
    wresbal = metrics_dict.get("WRESBAL")
    iorb = metrics_dict.get("IORB")
    policy_upper = metrics_dict.get("POLICY_UPPER_NYFED") or metrics_dict.get("DFEDTARU")
    effr = metrics_dict.get("EFFR")
    sofr = metrics_dict.get("SOFR")
    obfr = metrics_dict.get("OBFR")
    sofr_volume = metrics_dict.get("SOFR_VOLUME")
    tbill_size = metrics_dict.get("TBILL_AUCTION_SIZE")
    tbill_btc = metrics_dict.get("TBILL_AUCTION_BTC")
    usd = metrics_dict.get("DTWEXBGS")
    ig = metrics_dict.get("BAMLC0A0CM")
    hy = metrics_dict.get("BAMLH0A0HYM2")
    dgs1 = metrics_dict.get("DGS1")
    dgs3 = metrics_dict.get("DGS3")
    dgs10 = metrics_dict.get("DGS10")
    real_10y = metrics_dict.get("DGS10")
    curve_10y2y = metrics_dict.get("T10Y2Y")
    curve_10y3m = metrics_dict.get("T10Y3M")
    vix = metrics_dict.get("VIXCLS")
    nfci = metrics_dict.get("NFCI")

    nodes = [
        node("fed_liability", "Fed负债端水位", "TGA/RRP/WRESBAL 决定准备金缓冲空间", signal_status(["TGA_FLOW", "RRP_FLOW", "RRP_BUFFER"], ["TGA", "RRPONTSYD", "WRESBAL"]), [f"TGA {metric_value_text(tga)}", f"RRP Flow {signal_value_text(signal_map.get('RRP_FLOW'))}", f"RRP Buffer {signal_value_text(signal_map.get('RRP_BUFFER'))}", f"WRESBAL {metric_value_text(wresbal)}（周频背景）"], "先区分RRP边际流量和存量缓冲垫，再看负债端是否抽走或释放准备金。"),
        node("reserve_anchor", "政策锚/准备金边际", "IORB 是准备金报酬锚", signal_status(["SOFR_ANCHOR"], ["IORB"]), [f"IORB {metric_value_text(iorb)}", f"SOFR-Anchor {signal_value_text(signal_map.get('SOFR_ANCHOR'))}"], "SOFR接近或高于政策锚说明回购融资端准备金边际变紧。"),
        node("unsecured_funding", "银行间无抵押融资", "EFFR/OBFR", signal_status([], ["EFFR", "OBFR"]), [f"EFFR {metric_value_text(effr)}", f"OBFR {metric_value_text(obfr)}"], "银行间资金价格是否同步抬升。"),
        node("repo_collateral", "回购融资/抵押品链条", "SOFR/TGCR/BGCR + SOFR交易量 + T-bill吸收", signal_status(["SOFR_ANCHOR", "SOFR_VOLUME_IMPACT", "BGCR_TGCR", "TBILL_AUCTION_STRESS", "AUCTION_BTC"], ["SOFR", "SOFR_VOLUME", "TGCR", "BGCR", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC"]), [f"SOFR {metric_value_text(sofr)}", f"SOFR Volume {metric_value_text(sofr_volume)}", f"SOFR-Anchor {signal_value_text(signal_map.get('SOFR_ANCHOR'))}", f"T-bill Stress {signal_value_text(signal_map.get('TBILL_AUCTION_STRESS'))}", f"T-bill BTC {metric_value_text(tbill_btc)}"], "回购/抵押品融资压力，必须同时看价格偏离和承载该价格的交易量，以及T-bill供给×需求压力评分。"),
        node("bond_pricing", "债券定价锚/收益率曲线", "1Y/3Y/10Y", signal_status(["UST_1Y_YIELD", "REAL_10Y", "REAL_10Y_MOMENTUM", "UST_10Y2Y", "UST_10Y3M"], ["DGS1", "DGS3", "DGS10"]), [f"1Y {metric_value_text(dgs1)}", f"3Y {metric_value_text(dgs3)}", f"10Y {metric_value_text(dgs10)}", f"10Y Momentum {signal_value_text(signal_map.get('REAL_10Y_MOMENTUM'))}"], "用1Y看近端政策路径，3Y看中段再定价，10Y看长期折现率锚。"),
        node("offshore_usd", "离岸美元", "美元指数", signal_status(["USD_CHANGE"], ["DTWEXBGS"]), [f"DTWEXBGS {metric_value_text(usd)}"], "离岸美元融资压力。"),
        node("credit_market", "信用市场/金融条件", "CP/IG/HY/NFCI", signal_status(["CP_PROXY", "IG_CHANGE", "HY_CHANGE", "NFCI_LEVEL"], ["DCPN3M", "BAMLC0A0CM", "BAMLH0A0HYM2", "NFCI"]), [f"IG {metric_value_text(ig)}", f"HY {metric_value_text(hy)}", f"NFCI {metric_value_text(nfci)}"], "信用和金融条件传导。"),
        node("securities_risk", "证券市场风险偏好", "VIX", signal_status(["VIX_RISK", "VIX_MOMENTUM"], ["VIXCLS"]), [f"VIX {metric_value_text(vix)}", f"VIX Momentum {signal_value_text(signal_map.get('VIX_MOMENTUM'))}"], "股票波动率和避险需求；VIX上行只有在信用利差同步扩大时才说明压力进一步传导到信用融资。"),
    ]

    market_problem = next((item for item in nodes if item["problem_type"] == "market"), None)
    data_problem = next((item for item in nodes if item["problem_type"] == "data"), None)
    focus = market_problem or data_problem
    current_layer = focus["label"] if focus else "未发现明显断点"
    return {
        "nodes": nodes,
        "problem_layer": current_layer,
        "problem_type": focus["problem_type"] if focus else "none",
        "summary": f"当前问题主要位于{current_layer}。" if focus else "完整传导链未显示明显市场断点，继续监控负债端和短端融资。",
    }


def augment_charts_payload(charts_payload: Dict[str, Any], upcoming_auctions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Return charts payload enriched with deterministic dashboard-only chart series."""
    charts_payload = {**(charts_payload or {}), "charts": list((charts_payload or {}).get("charts", []))}
    existing_chart_ids = {chart.get("id") for chart in charts_payload.get("charts", [])}

    jpy_history = load_jpy_carry_history_payload()
    if jpy_history and jpy_history.get("charts"):
        jpy_charts = [chart for chart in jpy_history.get("charts", []) if chart.get("id") not in existing_chart_ids]
        if jpy_charts:
            charts_payload["charts"].extend(jpy_charts)
            existing_chart_ids.update(chart.get("id") for chart in jpy_charts)

    upcoming_chart_payloads = build_upcoming_auction_charts(upcoming_auctions)
    upcoming_charts = [chart for chart in upcoming_chart_payloads if chart.get("id") not in existing_chart_ids]
    if upcoming_charts:
        charts_payload["charts"].extend(upcoming_charts)
    return charts_payload


def build_dashboard_data(trigger: str, generated: str, context: Dict[str, Any], metrics: List[Metric], signals: List[DerivedSignal], charts_payload: Dict[str, Any], chart_paths: List[str], upcoming_auctions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data_as_of = latest_nonfuture_date([m.as_of for m in metrics])
    charts_payload = augment_charts_payload(charts_payload, upcoming_auctions)
    return {
        "meta": {
            "title": "美元流动性监测",
            "trigger": trigger or "默认运行",
            "generated_at_bjt": generated,
            "data_as_of": data_as_of,
            "timezone": "BJT",
            "theme": "warm_claude",
            "version": "1.0",
        },
        "status_scale": {
            "values": ["宽松", "中性偏松", "中性", "中性偏紧", "紧张"],
            "current_from_rule": context.get("stance"),
            "score_from_rule": context.get("score"),
        },
        "trading_dashboard": build_trading_dashboard(metrics, signals),
        "upcoming_auctions": upcoming_auctions or {},
        "jpy_carry": build_jpy_carry_overlay(metrics, signals),
        "indicator_groups": group_indicators(metrics),
        "derived_signals": [
            {
                "id": s.id, "label": s.name, "value": s.value,
                "value_text": format_number(s.value, s.unit),
                "previous": s.previous, "previous_text": format_number(s.previous, s.unit),
                "change": s.change, "change_text": format_signal_change(s.change, s.unit),
                "unit": s.unit, "severity": s.severity, "meaning": s.interpretation,
                "as_of": s.as_of,
            }
            for s in signals
        ],
        "core_indicator_impacts": [{"indicator": item[0], "importance": item[1], "reason": item[2]} for item in CORE_INDICATOR_IMPACTS],
        "charts": charts_payload.get("charts", []),
        "chart_paths": chart_paths,
        "data_quality": {
            "missing": [{"id": m.id, "label": rate_label(m.id), "reason": m.notes or m.status, "fallback": "详见缺失数据与替代指标"} for m in metrics if m.status != "ok"],
            "stale": [{"id": m.id, "label": rate_label(m.id), "stale_days": m.stale_days} for m in metrics if freshness_label(m) == "stale"],
            "degraded_sources": UNAVAILABLE_SOURCES,
        },
    }
