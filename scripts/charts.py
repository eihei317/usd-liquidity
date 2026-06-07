"""SVG chart generation and chart series fetching."""

from __future__ import annotations

import csv
import io
import json
import os
import sqlite3
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .utils import (
    BJT,
    UTC,
    OUTPUT_DIR,
    align_spread,
    chart_points,
    fiscal_amount_to_bn,
    get_fred_api_key,
    http_get_json,
    http_get_text,
    normalize_fred_value,
    parse_date_guess,
    read_tga_history,
    safe_float,
    trim_series,
)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")


# ─── Series fetching for charts ────────────────────────────────────────────────

def db_metric_series(metric_id: str, days: int) -> List[Tuple[str, float]]:
    """Read a metric time series from SQLite only, using the latest row per as_of date."""
    start_date = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT as_of, value FROM metrics_ts WHERE id IN ("
            "  SELECT MAX(id) FROM metrics_ts WHERE metric_id = ? AND as_of >= ? GROUP BY as_of"
            ") ORDER BY as_of",
            (metric_id, start_date)
        )
        return [(row[0], row[1]) for row in cur.fetchall() if row[1] is not None]
    finally:
        conn.close()


def db_derived_series(signal_id: str, days: int) -> List[Tuple[str, float]]:
    """Read a derived-signal time series from SQLite only, using the latest row per as_of date."""
    start_date = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT as_of, value FROM derived_signals_ts WHERE id IN ("
            "  SELECT MAX(id) FROM derived_signals_ts WHERE signal_id = ? AND as_of >= ? GROUP BY as_of"
            ") ORDER BY as_of",
            (signal_id, start_date)
        )
        return [(row[0], row[1]) for row in cur.fetchall() if row[1] is not None]
    finally:
        conn.close()


def fetch_fred_series_points(series_id: str, days: int, unit: str, use_cache: bool = True) -> List[Tuple[str, float]]:
    start_date = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    if use_cache:
        try:
            db_path = DB_PATH
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute(
                    "SELECT as_of, value FROM metrics_ts WHERE id IN ("
                    "  SELECT MAX(id) FROM metrics_ts WHERE metric_id = ? AND as_of >= ? GROUP BY as_of"
                    ") ORDER BY as_of",
                    (series_id, start_date)
                )
                rows = [(row[0], row[1]) for row in cur.fetchall() if row[1] is not None]
                conn.close()
                if len(rows) >= max(1, days // 3):
                    return rows
        except Exception:
            pass
    api_key = get_fred_api_key()
    if api_key:
        params = urllib.parse.urlencode({"series_id": series_id, "api_key": api_key, "file_type": "json", "sort_order": "asc", "observation_start": start_date})
        url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
        payload = http_get_json(url, timeout=12, retries=0)
        observations = payload.get("observations", []) if isinstance(payload, dict) else []
        rows: List[Tuple[str, float]] = []
        for row in observations:
            date = parse_date_guess(row.get("date"))
            value = safe_float(row.get("value"))
            if date and value is not None:
                rows.append((date, normalize_fred_value(series_id, value, unit)))
        try:
            if os.path.exists(DB_PATH):
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
                for d, v in rows:
                    cur.execute("INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at, snapshot_file) VALUES (?,?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at", (series_id, d, v, unit, "FRED API (chart cache)", ingested, "chart_cache"))
                conn.commit()
                conn.close()
        except Exception:
            pass
        return sorted(rows)

    params = urllib.parse.urlencode({"id": series_id, "cosd": start_date})
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?{params}"
    text = http_get_text(url, timeout=8, retries=0)
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        date = parse_date_guess(row.get("observation_date") or row.get("DATE") or row.get("date"))
        value = safe_float(row.get(series_id) or row.get("VALUE") or row.get("value"))
        if date and value is not None:
            rows.append((date, normalize_fred_value(series_id, value, unit)))
    return sorted(rows)


def _nyfed_series_to_db(metric_id: str, rates: List[Tuple[str, float]], policy_upper: List[Tuple[str, float]]) -> None:
    try:
        if not os.path.exists(DB_PATH):
            return
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
        for d, v in rates:
            cur.execute("INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at) VALUES (?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at", (metric_id.upper(), d, v, "%", "NY Fed Markets API (chart)", ingested))
        for d, v in policy_upper:
            cur.execute("INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at) VALUES (?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at", ("POLICY_UPPER_NYFED", d, v, "%", "NY Fed Markets API (chart)", ingested))
        conn.commit()
        conn.close()
    except Exception:
        pass


def _nyfed_series_from_db(metric_id: str, days: int) -> Tuple[Optional[List[Tuple[str, float]]], Optional[List[Tuple[str, float]]]]:
    try:
        if not os.path.exists(DB_PATH):
            return None, None
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        start = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
        cur.execute(
            "SELECT as_of, value FROM metrics_ts WHERE id IN ("
            "  SELECT MAX(id) FROM metrics_ts WHERE metric_id = ? AND as_of >= ? GROUP BY as_of"
            ") ORDER BY as_of",
            (metric_id.upper(), start)
        )
        rates = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        cur.execute(
            "SELECT as_of, value FROM metrics_ts WHERE id IN ("
            "  SELECT MAX(id) FROM metrics_ts WHERE metric_id = ? AND as_of >= ? GROUP BY as_of"
            ") ORDER BY as_of",
            ("POLICY_UPPER_NYFED", start)
        )
        policy = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        conn.close()
        if len(rates) >= max(1, days // 3) and len(policy) >= max(1, days // 3):
            return rates, policy
    except Exception:
        pass
    return None, None


def fetch_nyfed_rate_series(metric_id: str, secured: bool, days: int, use_cache: bool = True) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    if use_cache:
        cached_rates, cached_policy = _nyfed_series_from_db(metric_id, days)
        if cached_rates is not None:
            return cached_rates, cached_policy
    market = "secured" if secured else "unsecured"
    end = datetime.now(UTC).date()
    start = end - timedelta(days=days)
    params = urllib.parse.urlencode({"startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://markets.newyorkfed.org/api/rates/{market}/{metric_id}/search.json?{params}"
    payload = http_get_json(url, timeout=12, retries=0)
    records = payload.get("refRates", []) if isinstance(payload, dict) else []
    rates: List[Tuple[str, float]] = []
    policy_upper: List[Tuple[str, float]] = []
    for rec in records:
        date = parse_date_guess(rec.get("effectiveDate") or rec.get("date"))
        rate = safe_float(rec.get("percentRate") or rec.get("rate"))
        upper = safe_float(rec.get("targetRateTo"))
        if date and rate is not None:
            rates.append((date, rate))
        if date and upper is not None:
            policy_upper.append((date, upper))
    _nyfed_series_to_db(metric_id, rates, policy_upper)
    return sorted(rates), sorted(policy_upper)


def fetch_nyfed_volume_series(metric_id: str, secured: bool, days: int) -> List[Tuple[str, float]]:
    market = "secured" if secured else "unsecured"
    end = datetime.now(UTC).date()
    start = end - timedelta(days=days)
    params = urllib.parse.urlencode({"startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://markets.newyorkfed.org/api/rates/{market}/{metric_id}/search.json?{params}"
    payload = http_get_json(url, timeout=12, retries=0)
    records = payload.get("refRates", []) if isinstance(payload, dict) else []
    rows: List[Tuple[str, float]] = []
    for rec in records:
        date = parse_date_guess(rec.get("effectiveDate") or rec.get("date"))
        volume = safe_float(rec.get("volumeInBillions"))
        if date and volume is not None:
            rows.append((date, volume))
    return sorted(rows)


def fetch_tbill_auction_series(days: int) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    end = datetime.now(UTC).date()
    start = end - timedelta(days=days)
    params = urllib.parse.urlencode({"format": "json", "startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://www.treasurydirect.gov/TA_WS/securities/search?{params}"
    payload = http_get_json(url, timeout=12, retries=0)
    records = payload if isinstance(payload, list) else payload.get("data", []) if isinstance(payload, dict) else []
    grouped: Dict[str, Dict[str, float]] = {}
    for rec in records:
        if not isinstance(rec, dict) or str(rec.get("securityType", "")).lower() != "bill":
            continue
        date = parse_date_guess(rec.get("auctionDate") or rec.get("auction_date"))
        amount = fiscal_amount_to_bn(safe_float(rec.get("offeringAmount") or rec.get("offering_amount")))
        btc = safe_float(rec.get("bidToCoverRatio") or rec.get("bid_to_cover_ratio"))
        if not date or amount is None:
            continue
        bucket = grouped.setdefault(date, {"size": 0.0, "btc_weighted_sum": 0.0, "btc_weight": 0.0})
        bucket["size"] += amount
        if btc is not None:
            bucket["btc_weighted_sum"] += btc * amount
            bucket["btc_weight"] += amount
    size_rows: List[Tuple[str, float]] = []
    btc_rows: List[Tuple[str, float]] = []
    for date, bucket in sorted(grouped.items()):
        size_rows.append((date, bucket["size"]))
        if bucket["btc_weight"]:
            btc_rows.append((date, bucket["btc_weighted_sum"] / bucket["btc_weight"]))
    return size_rows, btc_rows


def _rrp_to_db(rows: List[Tuple[str, float]]) -> None:
    try:
        if not os.path.exists(DB_PATH):
            return
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
        for d, v in rows:
            cur.execute(
                "INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at) VALUES (?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at",
                ("RRPONTSYD", d, v, "USD bn", "NY Fed Markets API (chart)", ingested)
            )
        conn.commit()
        conn.close()
    except Exception:
        pass


def _rrp_from_db(days: int) -> Optional[List[Tuple[str, float]]]:
    try:
        if not os.path.exists(DB_PATH):
            return None
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        start = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
        cur.execute(
            "SELECT as_of, value FROM metrics_ts WHERE id IN ("
            "  SELECT MAX(id) FROM metrics_ts WHERE metric_id=? AND as_of>=? GROUP BY as_of"
            ") ORDER BY as_of",
            ("RRPONTSYD", start)
        )
        rows = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        conn.close()
        if len(rows) >= max(1, days // 3):
            return rows
    except Exception:
        pass
    return None


def fetch_rrp_series(days: int, use_cache: bool = True) -> List[Tuple[str, float]]:
    cached = _rrp_from_db(days) if use_cache else None
    if cached is not None:
        return cached
    end = datetime.now(UTC).date()
    start = end - timedelta(days=days)
    params = urllib.parse.urlencode({"startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://markets.newyorkfed.org/api/rp/reverserepo/positions/search.json?{params}"
    payload = http_get_json(url, timeout=12, retries=0)
    operations = payload.get("repo", {}).get("operations", []) if isinstance(payload, dict) else []
    rows: List[Tuple[str, float]] = []
    for rec in operations:
        date = parse_date_guess(rec.get("operationDate"))
        value = safe_float(rec.get("totalAmtAccepted"))
        if date and value is not None:
            rows.append((date, value / 1_000_000_000.0))
    rows = sorted(rows)
    _rrp_to_db(rows)
    return rows


def _tga_to_db(rows: List[Tuple[str, float]]) -> None:
    try:
        if not os.path.exists(DB_PATH):
            return
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
        for d, v in rows:
            cur.execute(
                "INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at) VALUES (?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at",
                ("TGA", d, v, "USD bn", "Treasury FiscalData API (chart)", ingested)
            )
        conn.commit()
        conn.close()
    except Exception:
        pass


def _tga_from_db(days: int) -> Optional[List[Tuple[str, float]]]:
    try:
        if not os.path.exists(DB_PATH):
            return None
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        start = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
        cur.execute(
            "SELECT as_of, value FROM metrics_ts WHERE id IN ("
            "  SELECT MAX(id) FROM metrics_ts WHERE metric_id=? AND as_of>=? GROUP BY as_of"
            ") ORDER BY as_of",
            ("TGA", start)
        )
        rows = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        conn.close()
        if len(rows) >= max(1, days // 3):
            return rows
    except Exception:
        pass
    return None


def fetch_tga_series(days: int, use_cache: bool = True) -> List[Tuple[str, float]]:
    cached = _tga_from_db(days) if use_cache else None
    if cached is not None:
        return cached
    page_size = max(30, min(120, days * 3))
    url = f"https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]={page_size}"
    payload = http_get_json(url, timeout=12, retries=0)
    records = payload.get("data", []) if isinstance(payload, dict) else []
    cutoff = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    rows: List[Tuple[str, float]] = []
    for rec in records:
        if "Closing Balance" not in str(rec.get("account_type", "")):
            continue
        date = parse_date_guess(rec.get("record_date"))
        raw_value = safe_float(rec.get("open_today_bal"))
        if raw_value is None:
            raw_value = safe_float(rec.get("close_today_bal"))
        value = fiscal_amount_to_bn(raw_value)
        if date and date >= cutoff and value is not None:
            rows.append((date, value))
    history = read_tga_history(90)
    existing_dates = {d for d, v in rows}
    for d, v in history:
        if d >= cutoff and d not in existing_dates:
            rows.append((d, v))
    rows = sorted(rows)
    _tga_to_db(rows)
    return rows


def fetch_chart_series(days: int = 40) -> Dict[str, List[Tuple[str, float]]]:
    """Build chart series from the SQLite history table only.

    Daily update flow is: fetch official data -> write snapshot -> ingest snapshot
    into SQLite -> read SQLite here to build frontend charts. This function must
    not call upstream APIs, otherwise the chart layer can diverge from the
    audited snapshot/model_input contract.
    """
    series: Dict[str, List[Tuple[str, float]]] = {}

    metric_ids = [
        "EFFR", "SOFR", "TGCR", "BGCR", "OBFR", "IORB", "POLICY_UPPER_NYFED",
        "SOFR_VOLUME", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC",
        "RRPONTSYD", "TGA", "DCPN3M", "DTB3", "DGS3MO", "DGS1", "DGS2",
        "DGS3", "DGS10", "DFII10", "DGS30", "T10Y2Y", "T10Y3M",
        "BAMLH0A0HYM2", "BAMLC0A0CM", "VIXCLS", "NFCI", "DTWEXBGS",
    ]
    for metric_id in metric_ids:
        rows = db_metric_series(metric_id, days)
        if rows:
            series[metric_id] = rows

    # Frontend charts use shorter aliases for balance-sheet series.
    if series.get("RRPONTSYD"):
        series["RRP"] = series["RRPONTSYD"]
    if series.get("IORB"):
        series["POLICY"] = series["IORB"]
    elif series.get("POLICY_UPPER_NYFED"):
        series["POLICY"] = series["POLICY_UPPER_NYFED"]

    # Prefer stored derived signals so chart values match the model input.
    for signal_id in ("SOFR_ANCHOR", "BGCR_TGCR", "CP_PROXY"):
        rows = db_derived_series(signal_id, days)
        if rows:
            series[signal_id] = rows

    # Fallback only from already-loaded DB rows, never from APIs.
    if not series.get("SOFR_ANCHOR") and series.get("SOFR") and series.get("POLICY"):
        series["SOFR_ANCHOR"] = align_spread(series["SOFR"], series["POLICY"])
    if not series.get("BGCR_TGCR") and series.get("BGCR") and series.get("TGCR"):
        series["BGCR_TGCR"] = align_spread(series["BGCR"], series["TGCR"])

    return series


# ─── SVG rendering ─────────────────────────────────────────────────────────────

def svg_escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_polyline(points: List[Tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def render_svg_panel(title: str, series_items: List[Tuple[str, List[Tuple[str, float]], str]], x: int, y: int, width: int, height: int, unit: str) -> str:
    non_empty = [(name, rows, color) for name, rows, color in series_items if rows]
    if not non_empty:
        return f'<g><text x="{x}" y="{y + 20}" font-size="15" font-weight="600">{svg_escape(title)}</text><text x="{x}" y="{y + 50}" font-size="13" fill="#777">暂无可绘制数据</text></g>'
    all_dates = sorted({date for _, rows, _ in non_empty for date, _ in rows})
    all_values = [value for _, rows, _ in non_empty for _, value in rows]
    min_v, max_v = min(all_values), max(all_values)
    if abs(max_v - min_v) < 1e-9:
        min_v -= 1.0
        max_v += 1.0
    pad = (max_v - min_v) * 0.12
    min_v -= pad
    max_v += pad
    left, right, top, bottom = x + 58, x + width - 18, y + 36, y + height - 34
    date_index = {date: idx for idx, date in enumerate(all_dates)}
    x_span = max(1, len(all_dates) - 1)

    def px(date: str) -> float:
        return left + (right - left) * date_index[date] / x_span

    def py(value: float) -> float:
        return bottom - (bottom - top) * (value - min_v) / (max_v - min_v)

    out = [f'<g><rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" fill="#ffffff" stroke="#e5e7eb"/>']
    out.append(f'<text x="{x + 16}" y="{y + 24}" font-size="15" font-weight="700" fill="#111827">{svg_escape(title)}</text>')
    for i in range(4):
        gy = top + (bottom - top) * i / 3
        val = max_v - (max_v - min_v) * i / 3
        out.append(f'<line x1="{left}" y1="{gy:.1f}" x2="{right}" y2="{gy:.1f}" stroke="#f3f4f6"/>')
        out.append(f'<text x="{x + 12}" y="{gy + 4:.1f}" font-size="10" fill="#6b7280">{val:.1f}{svg_escape(unit)}</text>')
    for name, rows, color in non_empty:
        pts = [(px(date), py(value)) for date, value in rows if date in date_index]
        if len(pts) == 1:
            out.append(f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="3" fill="{color}"/>')
        elif pts:
            out.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.2" points="{svg_polyline(pts)}"/>')
        label_x = x + 16 + 110 * (len(out) % 7)
        out.append(f'<circle cx="{label_x}" cy="{y + height - 12}" r="4" fill="{color}"/><text x="{label_x + 8}" y="{y + height - 8}" font-size="11" fill="#374151">{svg_escape(name)}</text>')
    out.append(f'<text x="{left}" y="{bottom + 20}" font-size="8" fill="#a8a29e">{svg_escape(all_dates[0])}</text>')
    out.append(f'<text x="{right - 58}" y="{bottom + 20}" font-size="8" fill="#a8a29e">{svg_escape(all_dates[-1])}</text>')
    out.append("</g>")
    return "".join(out)


def render_liquidity_svg(title: str, subtitle: str, days: int, series_bundle: Dict[str, List[Tuple[str, float]]]) -> str:
    anchor_label = "IORB" if series_bundle.get("IORB") else "政策锚"
    panels = [
        ("短端资金利率", [("EFFR", trim_series(series_bundle.get("EFFR", []), days), "#2563eb"), ("SOFR", trim_series(series_bundle.get("SOFR", []), days), "#dc2626"), ("TGCR", trim_series(series_bundle.get("TGCR", []), days), "#059669"), ("BGCR", trim_series(series_bundle.get("BGCR", []), days), "#7c3aed")], "%"),
        ("相对政策锚利差", [(f"SOFR-{anchor_label}", trim_series(series_bundle.get("SOFR_ANCHOR", []), days), "#dc2626")], "bp"),
        ("TGA财政现金余额", [("TGA", trim_series(series_bundle.get("TGA", []), days), "#0f766e")], "bn"),
        ("RRP缓冲余额", [("RRP", trim_series(series_bundle.get("RRP", []), days), "#9333ea")], "bn"),
    ]
    width, panel_h = 980, 210
    height = 90 + panel_h * len(panels)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">']
    out.append('<rect width="100%" height="100%" fill="#f8fafc"/>')
    out.append(f'<text x="28" y="34" font-size="22" font-weight="800" fill="#111827">{svg_escape(title)}</text>')
    out.append(f'<text x="28" y="58" font-size="13" fill="#64748b">{svg_escape(subtitle)}</text>')
    for idx, (panel_title, items, unit) in enumerate(panels):
        out.append(render_svg_panel(panel_title, items, 22, 78 + idx * panel_h, width - 44, panel_h - 18, unit))
    out.append('</svg>')
    return "".join(out)


def write_liquidity_charts(stamp: str, series_bundle: Optional[Dict[str, List[Tuple[str, float]]]] = None) -> List[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    series_bundle = series_bundle or fetch_chart_series(45)
    chart_specs = [
        ("7d", 10, "美元流动性核心指标：最近一周", "按最近10个日历日抓取，显示有效观测；日频指标按上一有效工作日比较"),
        ("30d", 35, "美元流动性核心指标：最近一月", "按最近35个日历日抓取，显示有效观测；TGA/RRP为十亿美元"),
    ]
    paths: List[Path] = []
    for suffix, days, title, subtitle in chart_specs:
        svg = render_liquidity_svg(title, subtitle, days, series_bundle)
        path = OUTPUT_DIR / f"usd_liquidity_chart_{suffix}_{stamp}.svg"
        path.write_text(svg, encoding="utf-8")
        paths.append(path)
    return paths
