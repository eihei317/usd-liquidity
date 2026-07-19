#!/usr/bin/env python3
"""Fetch JPY carry trade data and build frontend/model JSON packages.

Refactored to import shared utilities from scripts.utils.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Support running both as module and as standalone script
try:
    from .utils import (
        BJT, UTC, USER_AGENT, ROOT, OUTPUT_DIR, LATEST_DIR,
        get_fred_api_key, http_get_json, http_get_text,
        now_bjt, parse_date_guess, safe_float,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.utils import (
        BJT, UTC, USER_AGENT, ROOT, OUTPUT_DIR, LATEST_DIR,
        get_fred_api_key, http_get_json, http_get_text,
        now_bjt, parse_date_guess, safe_float,
    )

PROMPT_PATH = ROOT / "prompts" / "jpy_usd_carry_liquidity_prompt.md"


def latest_non_null(rows: List[Tuple[str, float]], offset: int = 0) -> Optional[Tuple[str, float]]:
    if len(rows) <= offset:
        return None
    return rows[-1 - offset]


def point_before(rows: List[Tuple[str, float]], latest_date: str, days: int) -> Optional[Tuple[str, float]]:
    """Return the latest observation on or before latest_date - days.

    Do not fall back to the first historical row when parsing/alignment fails;
    that turns daily changes into multi-year changes and pollutes carry signals.
    """
    base = parse_date_guess(latest_date)
    if not base:
        return None
    try:
        threshold = datetime.fromisoformat(base).date() - timedelta(days=days)
    except ValueError:
        return None
    candidates: List[Tuple[str, float]] = []
    for date, value in rows:
        parsed = parse_date_guess(date)
        if not parsed or len(parsed) < 10:
            continue
        try:
            if datetime.fromisoformat(parsed).date() <= threshold:
                candidates.append((parsed, value))
        except ValueError:
            continue
    return candidates[-1] if candidates else None


def pct_change(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    if current is None or previous is None or previous == 0:
        return None
    return (current / previous - 1.0) * 100.0


def realized_vol(rows: List[Tuple[str, float]], window: int = 20) -> Optional[float]:
    values = [v for _, v in rows[-(window + 1):] if v and v > 0]
    if len(values) < 6:
        return None
    returns = [math.log(values[i] / values[i - 1]) for i in range(1, len(values))]
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / max(1, len(returns) - 1)
    return math.sqrt(variance) * math.sqrt(252) * 100.0


def realized_vol_series(rows: List[Tuple[str, float]], window: int = 20) -> List[Tuple[str, float]]:
    normalized = normalize_rows(rows)
    out: List[Tuple[str, float]] = []
    for idx in range(window, len(normalized)):
        subset = normalized[idx - window:idx + 1]
        vol = realized_vol(subset, window)
        if vol is not None:
            out.append((normalized[idx][0], vol))
    return out


def normalize_rows(rows: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    """Normalize dates and sort rows, dropping unparsable dates."""
    out: List[Tuple[str, float]] = []
    for date, value in rows:
        parsed = parse_date_guess(date)
        if parsed and len(parsed) >= 10 and value is not None:
            out.append((parsed, value))
    return sorted(out)


def align_spread_previous_base(
    primary_rows: List[Tuple[str, float]],
    base_rows: List[Tuple[str, float]],
    multiplier: float = 100.0,
) -> List[Tuple[str, float]]:
    """Align primary series with the latest base observation not after each date."""
    primary = normalize_rows(primary_rows)
    base = normalize_rows(base_rows)
    if not primary or not base:
        return []
    out: List[Tuple[str, float]] = []
    idx = 0
    latest_base: Optional[Tuple[str, float]] = None
    for date, value in primary:
        while idx < len(base) and base[idx][0] <= date:
            latest_base = base[idx]
            idx += 1
        if latest_base is not None:
            out.append((date, (value - latest_base[1]) * multiplier))
    return out


def fetch_boj_series(db: str, code: str, start_yyyymm: str, end_yyyymm: str) -> Tuple[List[Tuple[str, float]], Dict[str, Any]]:
    params = urllib.parse.urlencode({"lang": "en", "db": db, "code": code, "startDate": start_yyyymm, "endDate": end_yyyymm})
    url = f"https://www.stat-search.boj.or.jp/api/v1/getDataCode?{params}"
    payload = http_get_json(url, timeout=20, retries=1)
    result = payload.get("RESULTSET", []) if isinstance(payload, dict) else []
    if not result:
        raise RuntimeError(f"BOJ returned no RESULTSET for {db}/{code}")
    series = result[0]
    values = series.get("VALUES", {})
    dates = values.get("SURVEY_DATES", []) or []
    nums = values.get("VALUES", []) or []
    rows: List[Tuple[str, float]] = []
    for date, value in zip(dates, nums):
        parsed = parse_date_guess(date)
        number = safe_float(value)
        if parsed and number is not None:
            rows.append((parsed, number))
    meta = {
        "name": series.get("NAME_OF_TIME_SERIES"),
        "unit": series.get("UNIT"),
        "frequency": series.get("FREQUENCY"),
        "last_update": series.get("LAST_UPDATE"),
        "source_url": url,
    }
    return rows, meta


def fetch_mof_jgb() -> Tuple[Dict[str, List[Tuple[str, float]]], Dict[str, Any]]:
    url = "https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/historical/jgbcme_all.csv"
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT}), timeout=25).read()
    text = raw.decode("shift_jis", errors="replace")
    lines = text.splitlines()
    reader = csv.DictReader(io.StringIO("\n".join(lines[1:])))
    out: Dict[str, List[Tuple[str, float]]] = {"JGB2": [], "JGB10": [], "JGB30": []}
    for row in reader:
        date = parse_date_guess(row.get("Date"))
        if not date:
            continue
        for key, col in (("JGB2", "2Y"), ("JGB10", "10Y"), ("JGB30", "30Y")):
            value = safe_float(row.get(col))
            if value is not None:
                out[key].append((date, value))
    return out, {"source_url": url, "frequency": "daily", "name": "MOF JGB constant-maturity yields"}


def fetch_cnbc_jgb() -> Tuple[Dict[str, Tuple[str, float]], Dict[str, Any]]:
    """Fetch latest Japan JGB constant-maturity yields (2Y/5Y/10Y/30Y) from the
    CNBC real-time bond quote API.

    Why this exists: MOF's historical CSV (fetch_mof_jgb) is the authoritative
    long-run source but has repeatedly stalled (last row 2026-06-29 in testing),
    leaving the JPY-carry JGB leg stuck ~3 weeks stale. CNBC's quote API returns
    the latest JGB yield per tenor to the most recent JST trading day (verified
    2026-07-18) without auth, so we use it to patch the latest point on top of
    MOF's history. The two are merged in build_payload.

    NOTE: CNBC's bond quote endpoint does NOT accept a comma-separated symbol
    list (it returns a single errored quote), so each tenor is fetched
    individually. JP10Y in particular has shown intermittent per-request
    failures (code 1 / no `last`) under the rapid sequential requests that the
    full pipeline makes right after several other network fetches. To make the
    JGB 10Y leg reliable we: (1) space tenor requests with a short delay to avoid
    tripping CNBC's rate limiting, (2) retry each tenor several times with a
    backoff, and (3) run a dedicated recovery pass that re-fetches any tenor that
    was still missing after the first pass (with a longer delay). Returns dict
    keyed JGB2/JGB5/JGB10/JGB30 -> (iso_date, yield_pct).
    """
    syms = ["JGB2", "JGB5", "JGB10", "JGB30"]
    sym_map = {"JGB2": "JP2Y", "JGB5": "JP5Y", "JGB10": "JP10Y", "JGB30": "JP30Y"}

    def fetch_one(key: str, retries: int, delay: float) -> Optional[Tuple[str, float]]:
        sym = sym_map[key]
        url = (
            "https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol"
            f"?symbols={sym}&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json"
        )
        for attempt in range(retries):
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
                )
                payload = json.loads(urllib.request.urlopen(req, timeout=15).read())
                quotes = payload.get("FormattedQuoteResult", {}).get("FormattedQuote", [{}])
                q = quotes[0] if quotes else {}
                if q.get("code") != 0 or not q.get("last"):
                    if attempt < retries - 1:
                        time.sleep(delay)
                    continue
                val = safe_float(str(q.get("last")).replace("%", ""))
                d = parse_date_guess(q.get("last_time")) if q.get("last_time") else None
                if val is not None and d:
                    return (d, val)
                if attempt < retries - 1:
                    time.sleep(delay)
            except Exception:
                if attempt < retries - 1:
                    time.sleep(delay)
                continue
        return None

    out: Dict[str, Tuple[str, float]] = {}
    for key in syms:
        pt = fetch_one(key, retries=5, delay=0.5)
        if pt:
            out[key] = pt
        time.sleep(0.5)

    # Recovery pass: JP10Y is the critical tenor for the user-facing JGB10 card and
    # the US-JP 10Y spread; if it (or any other tenor) dropped out, retry it on its
    # own with a longer spacing before we give up.
    missing = [k for k in syms if k not in out]
    for key in missing:
        time.sleep(1.5)
        pt = fetch_one(key, retries=6, delay=1.0)
        if pt:
            out[key] = pt
        time.sleep(1.0)

    if not out:
        raise RuntimeError("CNBC JGB quote API returned no usable tenors")
    return out, {"source": "CNBC", "source_url": "https://www.cnbc.com/bonds/", "frequency": "daily", "name": "CNBC real-time JGB yields (JP2Y/JP5Y/JP10Y/JP30Y)", "missing_tenors": missing}


def _decompose_cftc_net(short_chg: Optional[float], long_chg: Optional[float]) -> Dict[str, Any]:
    """把 CFTC 日元净空头的变化归因到：空头主动加仓 vs 多头平仓。

    决定性变量是 gross short 的边际方向：只有空头上升（short_building）才代表投机盘
    真实卖出日元、买入美元，即 carry 资金流在增强、对美元短期利好；若净空头变化并非
    来自新空头（多头平仓、或整体持仓缩减），则不能解读为 carry 在加杠杆。
    """
    if short_chg is None or long_chg is None:
        return {"driver": "unknown", "text": "CFTC 多/空分项周度变化不可用，无法区分净空头变多来自空头加仓还是多头平仓，应标记为数据缺口。"}
    if short_chg > 0:
        return {"driver": "short_building", "text": f"净空头变化中空头主动加仓（空头周变化 {short_chg:+,} 口、多头 {long_chg:+,} 口）：投机盘真实卖出日元、买入美元，carry 资金流在增强，对美元短期利好。"}
    if long_chg < 0:
        return {"driver": "long_unwinding", "text": f"净空头变化并非来自新空头，而是多头平仓主导（多头周变化 {long_chg:+,} 口、空头 {short_chg:+,} 口）：看多日元者离场，不能解读为 carry 资金流增强；若空头也同步下降，则整体持仓在缩减。"}
    return {"driver": "mixed", "text": f"净空头变化由空头 {short_chg:+,} 口、多头 {long_chg:+,} 口共同构成，方向不单一，需结合 short_share 判断。"}


def fetch_cftc_jpy(limit: int = 130) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    params = urllib.parse.urlencode({
        "cftc_contract_market_code": "097741",
        "$limit": limit,
        "$order": "report_date_as_yyyy_mm_dd DESC",
    })
    url = f"https://publicreporting.cftc.gov/resource/6dca-aqww.json?{params}"
    records = http_get_json(url, timeout=20, retries=1)
    rows: List[Dict[str, Any]] = []
    for rec in records if isinstance(records, list) else []:
        long_pos = safe_float(rec.get("noncomm_positions_long_all"))
        short_pos = safe_float(rec.get("noncomm_positions_short_all"))
        oi = safe_float(rec.get("open_interest_all"))
        if long_pos is None or short_pos is None:
            continue
        net = long_pos - short_pos
        short_share = (short_pos / (short_pos + long_pos)) if (short_pos + long_pos) else None
        rows.append({
            "date": parse_date_guess(rec.get("report_date_as_yyyy_mm_dd")),
            "net": net,
            "open_interest": oi,
            "net_oi": net / oi if oi else None,
            "long": long_pos,
            "short": short_pos,
            "short_share": short_share,
        })
    rows = [r for r in rows if r.get("date")]
    rows.sort(key=lambda r: r["date"])
    return rows, {"source_url": url, "frequency": "weekly", "name": "CFTC JPY futures non-commercial positioning"}


def fetch_fred_series_jpy(series_id: str, days: int) -> List[Tuple[str, float]]:
    start = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    api_key = get_fred_api_key()
    rows: List[Tuple[str, float]] = []
    if api_key:
        params = urllib.parse.urlencode({"series_id": series_id, "api_key": api_key, "file_type": "json", "sort_order": "asc", "observation_start": start})
        url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
        payload = http_get_json(url, timeout=20, retries=2)
        observations = payload.get("observations", []) if isinstance(payload, dict) else []
        for row in observations:
            date = parse_date_guess(row.get("date"))
            value = safe_float(row.get("value"))
            if date and value is not None:
                rows.append((date, value))
        return sorted(rows)

    params = urllib.parse.urlencode({"id": series_id, "cosd": start})
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?{params}"
    text = http_get_text(url, timeout=15, retries=1)
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        date = parse_date_guess(row.get("observation_date") or row.get("DATE") or row.get("date"))
        value = safe_float(row.get(series_id) or row.get("VALUE") or row.get("value"))
        if date and value is not None:
            rows.append((date, value))
    return sorted(rows)


def chart_points_jpy(rows: List[Tuple[str, float]], max_points: Optional[int] = None) -> List[Dict[str, Any]]:
    points = rows[-max_points:] if max_points else rows
    return [{"date": d, "value": v} for d, v in points]


def ensure_jpy_carry_table(conn: sqlite3.Connection) -> None:
    conn.execute('''
    CREATE TABLE IF NOT EXISTS jpy_carry_series_ts (
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
    conn.execute('CREATE INDEX IF NOT EXISTS idx_jpy_series_id_date ON jpy_carry_series_ts(series_id, as_of)')


def upsert_jpy_series(
    conn: sqlite3.Connection,
    series_id: str,
    series_name: str,
    category: str,
    rows: List[Tuple[str, float]],
    unit: str,
    source: str,
    source_url: str,
    snapshot_file: str,
    ingested_at: str,
    notes: str = "",
) -> int:
    inserted = 0
    for date, value in normalize_rows(rows):
        conn.execute(
            '''INSERT INTO jpy_carry_series_ts
                (series_id, series_name, category, as_of, value, unit, source, source_url, snapshot_file, ingested_at, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(series_id, as_of) DO UPDATE SET
                   value=excluded.value,
                   series_name=excluded.series_name,
                   category=excluded.category,
                   unit=excluded.unit,
                   source=excluded.source,
                   source_url=excluded.source_url,
                   ingested_at=excluded.ingested_at,
                   notes=excluded.notes''',
            (series_id, series_name, category, date, value, unit, source, source_url, snapshot_file, ingested_at, notes)
        )
        inserted += 1
    return inserted


def load_jpy_series_from_db(series_id: str, snapshot_file: Optional[str] = None, limit: Optional[int] = None) -> List[Tuple[str, float]]:
    """Load a JPY carry series from SQLite.

    By default (snapshot_file=None) this returns the FULL accumulated history for
    the series_id across all runs (the DB accumulates one row per (series_id, as_of)
    via upsert). Chart/history builders must use the full history so that an
    intermittent fetch failure in the current run (which would otherwise only
    persist its latest 1-2 points) does NOT shrink the rendered series to a single
    point. Pass snapshot_file only when you explicitly need one run's slice.
    """
    db_path = ROOT / "output" / "usd_liquidity.db"
    if not db_path.exists():
        return []
    conn = sqlite3.connect(str(db_path))
    try:
        ensure_jpy_carry_table(conn)
        cur = conn.cursor()
        if snapshot_file:
            cur.execute(
                '''SELECT as_of, value FROM jpy_carry_series_ts
                   WHERE series_id = ? AND snapshot_file = ?
                   ORDER BY as_of''',
                (series_id, snapshot_file)
            )
        else:
            cur.execute(
                '''SELECT as_of, value FROM jpy_carry_series_ts
                   WHERE series_id = ?
                   ORDER BY as_of''',
                (series_id,)
            )
        rows = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
    finally:
        conn.close()
    return rows[-limit:] if limit else rows


def persist_jpy_carry_series(series_map: Dict[str, Dict[str, Any]], snapshot_file: str, ingested_at: str) -> None:
    db_path = ROOT / "output" / "usd_liquidity.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    try:
        ensure_jpy_carry_table(conn)
        for series_id, meta in series_map.items():
            upsert_jpy_series(
                conn,
                series_id=series_id,
                series_name=meta.get("series_name", series_id),
                category=meta.get("category", "jpy_carry"),
                rows=meta.get("rows", []),
                unit=meta.get("unit", ""),
                source=meta.get("source", ""),
                source_url=meta.get("source_url", ""),
                snapshot_file=snapshot_file,
                ingested_at=ingested_at,
                notes=meta.get("notes", ""),
            )
        conn.commit()
    finally:
        conn.close()


def fmt_pct(value: Optional[float], digits: int = 2) -> str:
    return "NA" if value is None else f"{value:.{digits}f}%"


def fmt_signed_pct(value: Optional[float], digits: int = 2) -> str:
    return "NA" if value is None else f"{value:+.{digits}f}%"


def fmt_bp(value: Optional[float], digits: int = 1) -> str:
    return "NA" if value is None else f"{value:.{digits}f}bp"


def build_payload(trigger: str, stamp: Optional[str] = None) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    generated = now_bjt().strftime("%Y-%m-%d %H:%M:%S %Z")
    stamp = stamp or now_bjt().strftime("%Y%m%d_%H%M%S")
    snapshot_file = f"jpy_carry_history_{stamp}.json"
    end = now_bjt().strftime("%Y%m")
    start_daily = (now_bjt().date() - timedelta(days=395)).strftime("%Y%m")
    start_monthly = (now_bjt().date() - timedelta(days=1250)).strftime("%Y%m")
    notes: List[str] = []

    def safe_fetch(label: str, fn):
        try:
            return fn()
        except Exception as exc:
            notes.append(f"{label}: {exc}")
            return None

    boj_usdjpy = safe_fetch("BOJ USDJPY", lambda: fetch_boj_series("FM08", "FXERD04", start_daily, end))
    boj_call = safe_fetch("BOJ call rate", lambda: fetch_boj_series("FM01", "STRDCLUCON", start_daily, end))
    boj_neer = safe_fetch("BOJ NEER", lambda: fetch_boj_series("FM09", "FX180110001", start_monthly, end))
    boj_reer = safe_fetch("BOJ REER", lambda: fetch_boj_series("FM09", "FX180110002", start_monthly, end))
    mof = safe_fetch("MOF JGB", fetch_mof_jgb)
    cnbc_jgb, cnbc_jgb_meta = safe_fetch("CNBC JGB", fetch_cnbc_jgb) or ({}, {"source": "CNBC"})
    if cnbc_jgb_meta.get("missing_tenors"):
        notes.append(f"CNBC JGB 部分期限未能获取：{', '.join(cnbc_jgb_meta['missing_tenors'])}（该期限回退至 MOF 历史值）")
    cftc = safe_fetch("CFTC JPY", fetch_cftc_jpy)
    fred_dgs10 = safe_fetch("FRED DGS10", lambda: fetch_fred_series_jpy("DGS10", 420)) or []
    fred_dgs2 = safe_fetch("FRED DGS2", lambda: fetch_fred_series_jpy("DGS2", 420)) or []
    fred_vix = safe_fetch("FRED VIXCLS", lambda: fetch_fred_series_jpy("VIXCLS", 120)) or []
    fred_hy = safe_fetch("FRED HY OAS", lambda: fetch_fred_series_jpy("BAMLH0A0HYM2", 120)) or []

    usdjpy_rows, usdjpy_meta = boj_usdjpy if boj_usdjpy else ([], {"source_url": ""})
    call_rows, call_meta = boj_call if boj_call else ([], {"source_url": ""})
    neer_rows, neer_meta = boj_neer if boj_neer else ([], {"source_url": ""})
    reer_rows, reer_meta = boj_reer if boj_reer else ([], {"source_url": ""})
    jgb_mof, jgb_meta = mof if mof else ({"JGB2": [], "JGB10": [], "JGB30": []}, {"source_url": ""})
    dgs10_latest = latest_non_null(fred_dgs10)
    dgs10_latest_date = dgs10_latest[0] if dgs10_latest else None
    # Merge MOF long-run history with CNBC's fresher latest daily point. CNBC is
    # patched onto the DGS10 latest date too so the US-JP spread aligns to the same
    # trading day instead of forward-filling from MOF's stalled last row.
    jgb_rows: Dict[str, List[Tuple[str, float]]] = {}
    for term in ["JGB2", "JGB10", "JGB30"]:
        rows = list(jgb_mof.get(term, []))
        pt = cnbc_jgb.get(term)
        if pt:
            cdate, cval = pt
            rows = [r for r in rows if r[0] != cdate]
            rows.append((cdate, cval))
            if dgs10_latest_date and dgs10_latest_date <= cdate:
                rows = [r for r in rows if r[0] != dgs10_latest_date]
                rows.append((dgs10_latest_date, cval))
        jgb_rows[term] = normalize_rows(rows)
    if cnbc_jgb.get("JGB5"):
        cdate, cval = cnbc_jgb["JGB5"]
        rows5 = [(cdate, cval)]
        if dgs10_latest_date and dgs10_latest_date <= cdate:
            rows5.append((dgs10_latest_date, cval))
        jgb_rows["JGB5"] = normalize_rows(rows5)
    if cnbc_jgb:
        jgb_meta = {
            "source_url": jgb_meta.get("source_url", ""),
            "frequency": "daily",
            "name": "MOF JGB history + CNBC latest daily patch",
            "patch_source": cnbc_jgb_meta.get("source_url", "CNBC"),
        }
    cftc_rows, cftc_meta = cftc if cftc else ([], {"source_url": ""})

    usdjpy_latest = latest_non_null(usdjpy_rows)
    usdjpy_prev1 = point_before(usdjpy_rows, usdjpy_latest[0], 1) if usdjpy_latest else None
    usdjpy_prev20 = point_before(usdjpy_rows, usdjpy_latest[0], 20) if usdjpy_latest else None
    usdjpy_chg1 = (usdjpy_latest[1] - usdjpy_prev1[1]) if usdjpy_latest and usdjpy_prev1 else None
    usdjpy_chg1_pct = pct_change(usdjpy_latest[1], usdjpy_prev1[1]) if usdjpy_latest and usdjpy_prev1 else None
    usdjpy_chg20 = pct_change(usdjpy_latest[1], usdjpy_prev20[1]) if usdjpy_latest and usdjpy_prev20 else None
    usdjpy_vol20 = realized_vol(usdjpy_rows, 20)

    call_latest = latest_non_null(call_rows)
    call_prev1 = point_before(call_rows, call_latest[0], 1) if call_latest else None
    call_prev20 = point_before(call_rows, call_latest[0], 20) if call_latest else None
    call_chg1_bp = (call_latest[1] - call_prev1[1]) * 100 if call_latest and call_prev1 else None
    call_chg_bp = (call_latest[1] - call_prev20[1]) * 100 if call_latest and call_prev20 else None

    jgb10_latest = latest_non_null(jgb_rows.get("JGB10", []))
    jgb10_prev1 = point_before(jgb_rows.get("JGB10", []), jgb10_latest[0], 1) if jgb10_latest else None
    jgb10_prev60 = point_before(jgb_rows.get("JGB10", []), jgb10_latest[0], 60) if jgb10_latest else None
    jgb10_chg1_bp = (jgb10_latest[1] - jgb10_prev1[1]) * 100 if jgb10_latest and jgb10_prev1 else None
    jgb10_chg_bp = (jgb10_latest[1] - jgb10_prev60[1]) * 100 if jgb10_latest and jgb10_prev60 else None
    jgb2_latest = latest_non_null(jgb_rows.get("JGB2", []))
    jgb30_latest = latest_non_null(jgb_rows.get("JGB30", []))

    reer_latest = latest_non_null(reer_rows)
    reer_prev12 = point_before(reer_rows, reer_latest[0], 365) if reer_latest else None
    reer_chg12 = (reer_latest[1] - reer_prev12[1]) if reer_latest and reer_prev12 else None
    neer_latest = latest_non_null(neer_rows)

    cftc_latest = cftc_rows[-1] if cftc_rows else None
    cftc_prev = cftc_rows[-2] if len(cftc_rows) >= 2 else None
    cftc_net_oi = cftc_latest.get("net_oi") if cftc_latest else None
    cftc_change = (cftc_latest["net"] - cftc_prev["net"]) if cftc_latest and cftc_prev else None

    # --- Gross positioning decomposition: short vs long (多空分项) ---
    cftc_short = cftc_latest.get("short") if cftc_latest else None
    cftc_long = cftc_latest.get("long") if cftc_latest else None
    cftc_oi = cftc_latest.get("open_interest") if cftc_latest else None
    cftc_short_share = cftc_latest.get("short_share") if cftc_latest else None
    cftc_short_prev = cftc_prev.get("short") if cftc_prev else None
    cftc_long_prev = cftc_prev.get("long") if cftc_prev else None
    cftc_short_share_prev = cftc_prev.get("short_share") if cftc_prev else None
    cftc_short_chg = (cftc_short - cftc_short_prev) if (cftc_short is not None and cftc_short_prev is not None) else None
    cftc_long_chg = (cftc_long - cftc_long_prev) if (cftc_long is not None and cftc_long_prev is not None) else None
    cftc_short_share_chg = (cftc_short_share - cftc_short_share_prev) if (cftc_short_share is not None and cftc_short_share_prev is not None) else None
    # short_share 的近期极值分位（近1年），衡量空头一侧拥挤度
    cftc_short_share_series_all = [r["short_share"] for r in cftc_rows if r.get("short_share") is not None]
    cftc_short_share_pctile = None
    if cftc_short_share is not None and len(cftc_short_share_series_all) >= 52:
        cftc_short_share_pctile = sum(1 for x in cftc_short_share_series_all[-52:] if x <= cftc_short_share) / len(cftc_short_share_series_all[-52:])
    cftc_decomposition = _decompose_cftc_net(cftc_short_chg, cftc_long_chg)

    cftc_gross_short_series = [(r["date"], r["short"]) for r in cftc_rows if r.get("date") and r.get("short") is not None]
    cftc_gross_long_series = [(r["date"], r["long"]) for r in cftc_rows if r.get("date") and r.get("long") is not None]
    cftc_open_interest_series = [(r["date"], r["open_interest"]) for r in cftc_rows if r.get("date") and r.get("open_interest") is not None]
    cftc_short_share_series = [(r["date"], r["short_share"]) for r in cftc_rows if r.get("date") and r.get("short_share") is not None]

    dgs10_latest = latest_non_null(fred_dgs10)
    dgs2_latest = latest_non_null(fred_dgs2)
    us_jp_10y_series = align_spread_previous_base(fred_dgs10, jgb_rows.get("JGB10", []))
    us_jp_2y_series = align_spread_previous_base(fred_dgs2, jgb_rows.get("JGB2", []))
    usdjpy_vol20_series = realized_vol_series(usdjpy_rows, 20)
    cftc_net_oi_series = [(r["date"], r["net_oi"]) for r in cftc_rows if r.get("date") and r.get("net_oi") is not None]
    us_jp_10y_latest = latest_non_null(us_jp_10y_series)
    us_jp_2y_latest = latest_non_null(us_jp_2y_series)
    us_jp_10y = us_jp_10y_latest[1] if us_jp_10y_latest else None
    us_jp_2y = us_jp_2y_latest[1] if us_jp_2y_latest else None
    vix_latest = latest_non_null(fred_vix)
    hy_latest = latest_non_null(fred_hy)

    score = 0.0
    reasons: List[str] = []
    if cftc_net_oi is not None and cftc_net_oi <= -0.20:
        score += 1.5
        reasons.append("CFTC日元非商业净空头占未平仓合约比例偏高")
    if jgb10_chg_bp is not None and jgb10_chg_bp >= 20:
        score += 1.0
        reasons.append("JGB 10Y阶段性上行，日本本土收益率吸引力增强")
    if usdjpy_chg20 is not None and usdjpy_chg20 <= -2.0:
        score += 1.0
        reasons.append("USD/JPY近20日下跌，日元升值会触发carry回补")
    if usdjpy_vol20 is not None and usdjpy_vol20 >= 12:
        score += 1.0
        reasons.append("USD/JPY实现波动率上升，carry夏普下降")
    if vix_latest and vix_latest[1] >= 20:
        score += 1.0
        reasons.append("VIX上行，全球风险偏好转弱")
    if us_jp_10y is not None and us_jp_10y < 250:
        score += 0.5
        reasons.append("美日10Y利差处于相对较窄区域，收益端安全垫下降")

    if score >= 4:
        label = "偏高"
    elif score >= 2:
        label = "中性偏高"
    else:
        label = "中性"
    if not reasons:
        reasons.append("利差、汇率波动、仓位和全球风险偏好暂未形成unwind共振")

    def card(card_id, label_text, value_text, change_text, as_of, why):
        return {"id": card_id, "label": label_text, "value_text": value_text, "change_text": change_text, "as_of": as_of or "NA", "why": why}

    cards = [
        card("USDJPY", "USD/JPY（美元兑日元）", f"{usdjpy_latest[1]:.2f}" if usdjpy_latest else "NA", f"逐日 {fmt_signed_pct(usdjpy_chg1_pct)}" if usdjpy_chg1_pct is not None else "NA", usdjpy_latest[0] if usdjpy_latest else None, "日元快速升值会触发carry止损/回补"),
        card("JPY_CALL", "JPY隔夜融资成本（日本无担保隔夜拆借利率）", fmt_pct(call_latest[1], 3) if call_latest else "NA", f"逐日 {fmt_bp(call_chg1_bp)}" if call_chg1_bp is not None else "NA", call_latest[0] if call_latest else None, "carry trade 的融资端"),
        card("JGB10", "JGB 10Y（日本10年期国债收益率）", fmt_pct(jgb10_latest[1], 3) if jgb10_latest else "NA", f"逐日 {fmt_bp(jgb10_chg1_bp)}" if jgb10_chg1_bp is not None else "NA", jgb10_latest[0] if jgb10_latest else None, "日本本土资产吸引力和资金回流压力"),
        card("US_JP_10Y", "10Y UST-JGB利差（美日10年期国债利差）", fmt_bp(us_jp_10y, 0), "收益端核心", min(dgs10_latest[0], jgb10_latest[0]) if dgs10_latest and jgb10_latest else None, "美日长端利差越宽，carry收益端越顺风"),
        card("CFTC_JPY", "CFTC JPY净仓位/OI（日元期货非商业净仓位占比）", f"{cftc_net_oi:.1%}" if cftc_net_oi is not None else "NA", f"净周变化 {cftc_change:,.0f} 口" if cftc_change is not None else "NA", cftc_latest.get("date") if cftc_latest else None, f"净空头边际变化需拆分：{cftc_decomposition['text']}"),
        card("CFTC_JPY_GROSS_SHORT", "CFTC JPY非商业空头（总口数）", f"{cftc_short:,.0f}" if cftc_short is not None else "NA", f"周变化 {cftc_short_chg:,.0f} 口" if cftc_short_chg is not None else "NA", cftc_latest.get("date") if cftc_latest else None, "空头合约绝对量；周变化确认 carry 是否真在加仓（比 net/OI 更直接）"),
        card("CFTC_JPY_SHORT_SHARE", "CFTC JPY空头占比（空头/(空头+多头)）", f"{cftc_short_share:.1%}" if cftc_short_share is not None else "NA", f"周变化 {cftc_short_share_chg:+.1%}" if cftc_short_share_chg is not None else "NA", cftc_latest.get("date") if cftc_latest else None, (f"空头一侧真实强度代理；近1年分位 {cftc_short_share_pctile:.0%}" if cftc_short_share_pctile is not None else "空头一侧真实强度代理；净空头变多可能只是多头平仓，需看此值确认空头真加仓")),
        card("USDJPY_VOL20", "USD/JPY 20日实现波动率（年化）", fmt_pct(usdjpy_vol20), "年化", usdjpy_latest[0] if usdjpy_latest else None, "波动率上升会降低carry策略夏普"),
        card("JPY_REER", "JPY REER（日元实际有效汇率）", f"{reer_latest[1]:.2f}" if reer_latest else "NA", f"约12月 {reer_chg12:+.2f}" if reer_chg12 is not None else "NA", reer_latest[0] if reer_latest else None, "估值和政策敏感度背景"),
    ]

    sources = [
        {"name": "BOJ Time-Series Data Search API", "url": "https://www.stat-search.boj.or.jp/api/v1/getDataCode", "items": ["FM08/FXERD04 USDJPY", "FM01/STRDCLUCON call rate", "FM09 NEER/REER"]},
        {"name": "MOF JGB constant-maturity CSV (history)", "url": jgb_meta.get("source_url"), "items": ["2Y/10Y/30Y JGB yields long-run history"]},
        {"name": "CNBC real-time JGB yields (latest daily patch)", "url": cnbc_jgb_meta.get("source_url"), "items": ["JP2Y/JP5Y/JP10Y/JP30Y latest values"]},
        {"name": "CFTC Public Reporting API", "url": cftc_meta.get("source_url"), "items": ["JPY futures non-commercial positioning"]},
        {"name": "FRED", "url": "https://fred.stlouisfed.org/", "items": ["DGS2/DGS10", "VIXCLS", "BAMLH0A0HYM2"]},
    ]

    # Persist raw and engineered JPY carry series. Charts and model input below
    # read the engineered spreads back from SQLite, so spread values are an
    # auditable engineering output rather than model-side math.
    persist_jpy_carry_series({
        "USDJPY": {"series_name": "USD/JPY", "category": "fx", "rows": usdjpy_rows, "unit": "JPY per USD", "source": "BOJ", "source_url": usdjpy_meta.get("source_url", "")},
        "JPY_CALL": {"series_name": "JPY overnight call rate", "category": "funding", "rows": call_rows, "unit": "%", "source": "BOJ", "source_url": call_meta.get("source_url", "")},
        "JGB2": {"series_name": "JGB 2Y", "category": "jgb", "rows": jgb_rows.get("JGB2", []), "unit": "%", "source": "MOF+CNBC", "source_url": jgb_meta.get("source_url", "")},
        "JGB5": {"series_name": "JGB 5Y", "category": "jgb", "rows": jgb_rows.get("JGB5", []), "unit": "%", "source": "CNBC", "source_url": cnbc_jgb_meta.get("source_url", "")},
        "JGB10": {"series_name": "JGB 10Y", "category": "jgb", "rows": jgb_rows.get("JGB10", []), "unit": "%", "source": "MOF+CNBC", "source_url": jgb_meta.get("source_url", "")},
        "JGB30": {"series_name": "JGB 30Y", "category": "jgb", "rows": jgb_rows.get("JGB30", []), "unit": "%", "source": "MOF+CNBC", "source_url": jgb_meta.get("source_url", "")},
        "DGS2": {"series_name": "US Treasury 2Y", "category": "ust", "rows": fred_dgs2, "unit": "%", "source": "FRED", "source_url": "https://fred.stlouisfed.org/series/DGS2"},
        "DGS10": {"series_name": "US Treasury 10Y", "category": "ust", "rows": fred_dgs10, "unit": "%", "source": "FRED", "source_url": "https://fred.stlouisfed.org/series/DGS10"},
        "JPY_NEER": {"series_name": "JPY NEER", "category": "effective_fx", "rows": neer_rows, "unit": "index", "source": "BOJ", "source_url": neer_meta.get("source_url", "")},
        "JPY_REER": {"series_name": "JPY REER", "category": "effective_fx", "rows": reer_rows, "unit": "index", "source": "BOJ", "source_url": reer_meta.get("source_url", "")},
        "CFTC_JPY_NET_OI": {"series_name": "CFTC JPY net position / open interest", "category": "positioning", "rows": cftc_net_oi_series, "unit": "net/OI", "source": "CFTC", "source_url": cftc_meta.get("source_url", ""), "notes": "non-commercial net / open interest"},
        "CFTC_JPY_GROSS_SHORT": {"series_name": "CFTC JPY non-commercial gross short", "category": "positioning", "rows": cftc_gross_short_series, "unit": "contracts", "source": "CFTC", "source_url": cftc_meta.get("source_url", ""), "notes": "non-commercial short positions, gross"},
        "CFTC_JPY_GROSS_LONG": {"series_name": "CFTC JPY non-commercial gross long", "category": "positioning", "rows": cftc_gross_long_series, "unit": "contracts", "source": "CFTC", "source_url": cftc_meta.get("source_url", ""), "notes": "non-commercial long positions, gross"},
        "CFTC_JPY_SHORT_SHARE": {"series_name": "CFTC JPY short share", "category": "positioning", "rows": cftc_short_share_series, "unit": "short/(short+long)", "source": "CFTC", "source_url": cftc_meta.get("source_url", ""), "notes": "gross short / (gross short + gross long): short-side intensity proxy"},
        "CFTC_JPY_OPEN_INTEREST": {"series_name": "CFTC JPY open interest", "category": "positioning", "rows": cftc_open_interest_series, "unit": "contracts", "source": "CFTC", "source_url": cftc_meta.get("source_url", ""), "notes": "total open interest all"},
        "USDJPY_VOL20": {"series_name": "USD/JPY 20D realized volatility", "category": "engineered_volatility", "rows": usdjpy_vol20_series, "unit": "%", "source": "engineered", "source_url": "", "notes": "20-observation annualized realized volatility from USDJPY"},
        "US_JP_2Y": {"series_name": "2Y UST-JGB spread", "category": "engineered_spread", "rows": us_jp_2y_series, "unit": "bp", "source": "engineered", "source_url": "", "notes": "DGS2 minus latest JGB2 not after each US date"},
        "US_JP_10Y": {"series_name": "10Y UST-JGB spread", "category": "engineered_spread", "rows": us_jp_10y_series, "unit": "bp", "source": "engineered", "source_url": "", "notes": "DGS10 minus latest JGB10 not after each US date"},
    }, snapshot_file=snapshot_file, ingested_at=generated)
    # Load the FULL accumulated history for each series (snapshot_file=None) so the
    # rendered charts/history use the complete DB time series even if the current
    # run's live fetch was incomplete.
    usdjpy_chart_rows = load_jpy_series_from_db("USDJPY", limit=260)
    call_chart_rows = load_jpy_series_from_db("JPY_CALL", limit=260)
    jgb2_chart_rows = load_jpy_series_from_db("JGB2", limit=260)
    jgb10_chart_rows = load_jpy_series_from_db("JGB10", limit=260)
    jgb30_chart_rows = load_jpy_series_from_db("JGB30", limit=260)
    cftc_net_oi_chart_rows = load_jpy_series_from_db("CFTC_JPY_NET_OI")
    cftc_gross_short_chart_rows = load_jpy_series_from_db("CFTC_JPY_GROSS_SHORT")
    cftc_gross_long_chart_rows = load_jpy_series_from_db("CFTC_JPY_GROSS_LONG")
    cftc_short_share_chart_rows = load_jpy_series_from_db("CFTC_JPY_SHORT_SHARE")
    cftc_open_interest_chart_rows = load_jpy_series_from_db("CFTC_JPY_OPEN_INTEREST")
    usdjpy_vol20_chart_rows = load_jpy_series_from_db("USDJPY_VOL20")
    neer_chart_rows = load_jpy_series_from_db("JPY_NEER")
    reer_chart_rows = load_jpy_series_from_db("JPY_REER")
    us_jp_2y_series = load_jpy_series_from_db("US_JP_2Y")
    us_jp_10y_series = load_jpy_series_from_db("US_JP_10Y")

    charts = [
        {"id": "jpy_usdjpy_funding_1y", "title": "JPY Carry：USD/JPY 与日元隔夜融资成本", "chart_type": "line", "unit": "", "dual_axis": True, "y_axes": {"y": "USD/JPY", "y1": "%"}, "data_source": "SQLite jpy_carry_series_ts", "series": [
            {"id": "USDJPY", "label": "USD/JPY（东京17:00）", "points": chart_points_jpy(usdjpy_chart_rows), "y_axis": "y"},
            {"id": "JPY_CALL", "label": "JPY隔夜融资成本", "points": chart_points_jpy(call_chart_rows), "y_axis": "y1"},
        ]},
        {"id": "jpy_jgb_curve_1y", "title": "JGB收益率：2Y / 10Y / 30Y", "chart_type": "line", "unit": "%", "data_source": "SQLite jpy_carry_series_ts", "series": [
            {"id": "JGB2", "label": "JGB 2Y", "points": chart_points_jpy(jgb2_chart_rows)},
            {"id": "JGB10", "label": "JGB 10Y", "points": chart_points_jpy(jgb10_chart_rows)},
            {"id": "JGB30", "label": "JGB 30Y", "points": chart_points_jpy(jgb30_chart_rows)},
        ]},
        {"id": "jpy_cftc_position_2y", "title": "CFTC JPY仓位拥挤度", "chart_type": "line", "unit": "net/OI", "data_source": "SQLite jpy_carry_series_ts.CFTC_JPY_NET_OI", "series": [
            {"id": "CFTC_JPY_NET_OI", "label": "JPY非商业净仓位/OI", "points": chart_points_jpy(cftc_net_oi_chart_rows)},
        ]},
        {"id": "jpy_effective_fx_3y", "title": "JPY NEER / REER", "chart_type": "line", "unit": "index", "data_source": "SQLite jpy_carry_series_ts", "series": [
            {"id": "JPY_NEER", "label": "JPY NEER", "points": chart_points_jpy(neer_chart_rows)},
            {"id": "JPY_REER", "label": "JPY REER", "points": chart_points_jpy(reer_chart_rows)},
        ]},
        {"id": "us_jp_spread", "title": "美日利差代理", "chart_type": "line", "unit": "bp", "data_source": "SQLite jpy_carry_series_ts.US_JP_2Y/US_JP_10Y", "series": [
            {"id": "US_JP_2Y", "label": "2Y UST-JGB", "points": chart_points_jpy(us_jp_2y_series[-260:])},
            {"id": "US_JP_10Y", "label": "10Y UST-JGB", "points": chart_points_jpy(us_jp_10y_series[-260:])},
        ]},
        {"id": "jpy_cftc_gross_2y", "title": "CFTC JPY：空头 vs 多头（非商业，验证空头是否真加仓）", "chart_type": "line", "unit": "contracts", "data_source": "SQLite jpy_carry_series_ts", "series": [
            {"id": "CFTC_JPY_GROSS_SHORT", "label": "非商业空头", "points": chart_points_jpy(cftc_gross_short_chart_rows[-104:])},
            {"id": "CFTC_JPY_GROSS_LONG", "label": "非商业多头", "points": chart_points_jpy(cftc_gross_long_chart_rows[-104:])},
        ]},
        {"id": "jpy_cftc_short_share_2y", "title": "CFTC JPY空头占比（空头/(空头+多头)，空头一侧真实强度）", "chart_type": "line", "unit": "short/(short+long)", "data_source": "SQLite jpy_carry_series_ts", "series": [
            {"id": "CFTC_JPY_SHORT_SHARE", "label": "空头占比", "points": chart_points_jpy(cftc_short_share_chart_rows[-104:])},
        ]},
    ]

    jpy_carry = {
        "meta": {"generated_at_bjt": generated, "lookback": "日频约1年，CFTC约2年，REER/NEER约3年"},
        "risk": {"label": label, "score": round(score, 1), "reasons": reasons[:5]},
        "cards": cards,
        "cftc_decomposition": cftc_decomposition,
        "history": {
            "USDJPY": chart_points_jpy(usdjpy_chart_rows),
            "JPY_CALL": chart_points_jpy(call_chart_rows),
            "JGB10": chart_points_jpy(jgb10_chart_rows),
            "US_JP_10Y": chart_points_jpy(us_jp_10y_series),
            "CFTC_JPY_NET_OI": chart_points_jpy(cftc_net_oi_chart_rows),
            "CFTC_JPY_GROSS_SHORT": chart_points_jpy(cftc_gross_short_chart_rows),
            "CFTC_JPY_GROSS_LONG": chart_points_jpy(cftc_gross_long_chart_rows),
            "CFTC_JPY_SHORT_SHARE": chart_points_jpy(cftc_short_share_chart_rows),
            "CFTC_JPY_OPEN_INTEREST": chart_points_jpy(cftc_open_interest_chart_rows),
            "USDJPY_VOL20": chart_points_jpy(usdjpy_vol20_chart_rows),
        },
        "sources": sources,
        "notes": notes,
    }
    history = {"jpy_carry": jpy_carry, "charts": charts}

    analysis = {
        "meta": {"generated_at_bjt": generated, "model": "rule_summary", "prompt_file": str(PROMPT_PATH), "note": "模型分析可基于 jpy_carry_model_input.json 覆盖本文件。"},
        "risk": jpy_carry["risk"],
        "one_liner": f"日元 carry unwind 风险为{label}；" + "；".join(reasons[:2]),
        "dashboard_modules": (lambda cb: [
            {"module": "日元融资端", "status": "低位但需观察", "evidence": cb["JPY_CALL"]["value_text"], "explanation": cb["JPY_CALL"]["why"]},
            {"module": "美日利差", "status": "仍有carry收益", "evidence": cb["US_JP_10Y"]["value_text"], "explanation": cb["US_JP_10Y"]["why"]},
            {"module": "汇率与波动", "status": "未触发unwind", "evidence": f"{cb['USDJPY']['value_text']} / vol {cb['USDJPY_VOL20']['value_text']}", "explanation": "快速日元升值和波动率上升才是核心触发。"},
            {"module": "仓位拥挤度(净)", "status": "拥挤" if cftc_net_oi is not None and cftc_net_oi <= -0.2 else "中性", "evidence": cb["CFTC_JPY"]["value_text"], "explanation": cb["CFTC_JPY"]["why"]},
            {"module": "空头真实强度", "status": ("加仓" if cftc_decomposition["driver"] == "short_building" else "中性" if cftc_decomposition["driver"] in ("mixed", "unknown") else "平仓主导"), "evidence": cb["CFTC_JPY_SHORT_SHARE"]["value_text"], "explanation": cftc_decomposition["text"]},
        ])({c["id"]: c for c in cards}),
        "watchlist": ["USD/JPY 20日实现波动率", "CFTC JPY净仓位/OI", "CFTC JPY空头占比(空头/(空头+多头))", "10Y UST-JGB利差", "VIX/HY OAS"],
    }

    prompt = PROMPT_PATH.read_text(encoding="utf-8") if PROMPT_PATH.exists() else ""
    model_input = {
        "task": "基于美元流动性数据与日元 carry overlay 数据，输出可被固定前端读取的结构化 jpy_carry_analysis.json。",
        "trigger": trigger or "更新 JPY carry 数据",
        "generated_at_bjt": generated,
        "prompt_file": str(PROMPT_PATH),
        "analysis_prompt": prompt,
        "data": history,
        "output_contract": {
            "format": "strict_json_only",
            "language": "中文",
            "required_top_level_fields": ["meta", "risk", "one_liner", "dashboard_modules", "watchlist"],
            "frontend_rule": "前端读取 output/latest/jpy_carry_history.json 和/或 dashboard_data.json.jpy_carry；模型只覆盖 jpy_carry_analysis.json，不生成HTML。",
        },
    }
    return history, analysis, model_input


def write_outputs_jpy(history: Dict[str, Any], analysis: Dict[str, Any], model_input: Dict[str, Any], stamp: str) -> Dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "history_path": OUTPUT_DIR / f"jpy_carry_history_{stamp}.json",
        "analysis_path": OUTPUT_DIR / f"jpy_carry_analysis_{stamp}.json",
        "model_input_path": OUTPUT_DIR / f"jpy_carry_model_input_{stamp}.json",
    }
    paths["history_path"].write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["analysis_path"].write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["model_input_path"].write_text(json.dumps(model_input, ensure_ascii=False, indent=2), encoding="utf-8")
    (LATEST_DIR / "jpy_carry_history.json").write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    (LATEST_DIR / "jpy_carry_analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    (LATEST_DIR / "jpy_carry_model_input.json").write_text(json.dumps(model_input, ensure_ascii=False, indent=2), encoding="utf-8")
    return paths


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch JPY carry trade history and build model input JSON")
    parser.add_argument("trigger", nargs="*", help="Natural-language trigger")
    parser.add_argument("--json", action="store_true", help="Print output paths as JSON")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    trigger = " ".join(args.trigger).strip()
    stamp = now_bjt().strftime("%Y%m%d_%H%M%S")
    history, analysis, model_input = build_payload(trigger, stamp)
    paths = write_outputs_jpy(history, analysis, model_input, stamp)
    result = {key: str(value) for key, value in paths.items()}
    result.update({"latest_dir": str(LATEST_DIR), "risk_label": history["jpy_carry"]["risk"]["label"], "risk_score": history["jpy_carry"]["risk"]["score"]})
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"JPY carry 风险：{result['risk_label']} | 分数：{result['risk_score']}")
        print(f"历史数据：{result['history_path']}")
        print(f"模型输入：{result['model_input_path']}")
        print(f"分析结果：{result['analysis_path']}")
        print(f"最新目录：{LATEST_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
