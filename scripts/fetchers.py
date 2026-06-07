"""All fetch_* data-fetching functions (NY Fed, FRED, Treasury, OFR, CFTC)."""

from __future__ import annotations

import concurrent.futures
import csv
import io
import json
import math
import time
import urllib.parse
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from .utils import (
    BJT,
    UTC,
    USER_AGENT,
    Metric,
    append_tga_history,
    error_metric,
    fiscal_amount_to_bn,
    get_fred_api_key,
    http_get_json,
    http_get_text,
    make_metric,
    metric_map,
    normalize_fred_value,
    parse_date_guess,
    read_tga_history,
    redact_url_secret,
    safe_float,
    walk_dicts,
)


def extract_nyfed_observations(payload: Any) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for d in walk_dicts(payload):
        keys = set(d.keys())
        has_date = bool(keys & {"effectiveDate", "date", "businessDate", "referenceDate"})
        has_rate = bool(keys & {"percentRate", "rate", "averageRate", "ratePercent"})
        if has_date and has_rate:
            candidates.append(d)
    return candidates


def fetch_nyfed_rate(metric_id: str, name: str, secured: bool) -> Metric:
    market = "secured" if secured else "unsecured"
    url = f"https://markets.newyorkfed.org/api/rates/{market}/{metric_id}/last/2.json"
    try:
        payload = http_get_json(url)
        records = extract_nyfed_observations(payload)
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in records:
            date = parse_date_guess(rec.get("effectiveDate") or rec.get("date") or rec.get("businessDate") or rec.get("referenceDate"))
            value = safe_float(rec.get("percentRate") or rec.get("rate") or rec.get("averageRate") or rec.get("ratePercent"))
            if date and value is not None:
                parsed.append((date, value, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"raw_latest": parsed[-1][2]} if parsed else {}
        return make_metric(metric_id.upper(), name, "银行间/回购融资", latest, previous, "%", "daily T+1", "NY Fed Markets API", url, extra=extra)
    except Exception as exc:
        return error_metric(metric_id.upper(), name, "银行间/回购融资", "%", "daily T+1", "NY Fed Markets API", url, exc)


def fetch_nyfed_sofr_volume() -> Metric:
    """Fetch SOFR transaction volume from the NY Fed reference-rate record."""
    url = "https://markets.newyorkfed.org/api/rates/secured/sofr/last/2.json"
    try:
        payload = http_get_json(url)
        records = extract_nyfed_observations(payload)
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in records:
            date = parse_date_guess(rec.get("effectiveDate") or rec.get("date") or rec.get("businessDate") or rec.get("referenceDate"))
            value = safe_float(rec.get("volumeInBillions"))
            if date and value is not None:
                parsed.append((date, value, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"raw_latest": parsed[-1][2]} if parsed else {}
        notes = "SOFR transaction volume reported by NY Fed in billions of dollars; use with SOFR-Policy spread to estimate price × size impact."
        return make_metric("SOFR_VOLUME", "SOFR transaction volume", "回购融资/市场深度", latest, previous, "USD bn", "daily T+1", "NY Fed Markets API", url, notes=notes, extra=extra)
    except Exception as exc:
        return error_metric("SOFR_VOLUME", "SOFR transaction volume", "回购融资/市场深度", "USD bn", "daily T+1", "NY Fed Markets API", url, exc)


def fetch_fred_series(series_id: str, name: str, category: str, unit: str, frequency: str) -> Metric:
    start_date = (datetime.now(UTC).date() - timedelta(days=180)).isoformat()
    source_page_url = f"https://fred.stlouisfed.org/series/{series_id}"
    api_key = get_fred_api_key()
    if api_key:
        params = urllib.parse.urlencode({"series_id": series_id, "api_key": api_key, "file_type": "json", "sort_order": "desc", "limit": 2, "observation_start": start_date})
        url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
        source = "FRED API"
    else:
        params = urllib.parse.urlencode({"id": series_id, "cosd": start_date})
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?{params}"
        source = "FRED CSV"
    try:
        rows: List[Tuple[str, float]] = []
        if api_key:
            payload = http_get_json(url, timeout=12, retries=2)
            observations = payload.get("observations", []) if isinstance(payload, dict) else []
            for row in observations:
                date = parse_date_guess(row.get("date"))
                value = safe_float(row.get("value"))
                if date and value is not None:
                    rows.append((date, normalize_fred_value(series_id, value, unit)))
        else:
            text = http_get_text(url, timeout=8, retries=0)
            reader = csv.DictReader(io.StringIO(text))
            for row in reader:
                date = parse_date_guess(row.get("observation_date") or row.get("DATE") or row.get("date"))
                value = safe_float(row.get(series_id) or row.get("VALUE") or row.get("value"))
                if date and value is not None:
                    rows.append((date, normalize_fred_value(series_id, value, unit)))
        rows = sorted(rows, key=lambda x: x[0])
        latest = rows[-1] if rows else None
        previous = rows[-2] if len(rows) >= 2 else None
        return make_metric(series_id, name, category, latest, previous, unit, frequency, source, source_page_url, extra={"fetch_url": redact_url_secret(url)})
    except Exception as exc:
        safe_exc = RuntimeError(str(exc).replace(api_key, "REDACTED")) if api_key else exc
        metric = error_metric(series_id, name, category, unit, frequency, source, source_page_url, safe_exc)
        metric.extra = {"fetch_url": redact_url_secret(url)}
        return metric


def fetch_tga() -> Metric:
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]=90"
    try:
        payload = http_get_json(url)
        records = payload.get("data", []) if isinstance(payload, dict) else []
        parsed: List[Tuple[str, float]] = []
        for rec in records:
            account_type = str(rec.get("account_type", ""))
            if "Closing Balance" not in account_type:
                continue
            date = parse_date_guess(rec.get("record_date"))
            raw_value = safe_float(rec.get("open_today_bal") or rec.get("close_today_bal"))
            value = fiscal_amount_to_bn(raw_value)
            if date and value is not None:
                parsed.append((date, value))
        parsed = sorted(set(parsed), key=lambda x: x[0])
        if not parsed:
            return error_metric("TGA", "Treasury General Account / operating cash balance", "Fed负债端", "USD bn", "daily T+1", "Treasury FiscalData", url, Exception("no data"))
        for d, v in parsed:
            append_tga_history(d, v)
        latest_date, latest_value = parsed[-1]
        history = read_tga_history(90)
        previous = None
        for d, v in reversed(history):
            if d < latest_date:
                previous = (d, v)
                break
        extra = {"raw_latest": records[0]} if records else {}
        metric = make_metric("TGA", "Treasury General Account closing balance", "Fed负债端",
                            (latest_date, latest_value), previous,
                            "USD bn", "daily T+1", "Treasury FiscalData", url, extra=extra)
        return metric
    except Exception as exc:
        return error_metric("TGA", "Treasury General Account / operating cash balance", "Fed负债端", "USD bn", "daily T+1", "Treasury FiscalData", url, exc)


def fetch_nyfed_rrp(lookback_days: int = 14) -> Metric:
    end = datetime.now(UTC).date()
    start = end - timedelta(days=lookback_days)
    params = urllib.parse.urlencode({"startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json?{params}"
    try:
        payload = http_get_json(url)
        operations = []
        if isinstance(payload, dict):
            operations = payload.get("repo", {}).get("operations", [])
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in operations:
            date = parse_date_guess(rec.get("operationDate"))
            value = safe_float(rec.get("totalAmtAccepted"))
            if date and value is not None:
                parsed.append((date, value / 1_000_000_000.0, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"raw_latest": parsed[-1][2], "lookback_days": lookback_days} if parsed else {"lookback_days": lookback_days}
        status = "ok" if latest else "unavailable"
        notes = "NY Fed reverse repo accepted amount; replaces FRED RRPONTSYD when FRED is slow or unavailable"
        return make_metric("RRPONTSYD", "Overnight Reverse Repo accepted amount", "Fed负债端", latest, previous, "USD bn", "daily T+1", "NY Fed Markets API", url, status=status, notes=notes, extra=extra)
    except Exception as exc:
        return error_metric("RRPONTSYD", "Overnight Reverse Repo accepted amount", "Fed负债端", "USD bn", "daily T+1", "NY Fed Markets API", url, exc)


def fetch_soma_summary() -> Metric:
    url = "https://markets.newyorkfed.org/api/soma/summary.json"
    try:
        payload = http_get_json(url)
        records = list(walk_dicts(payload))
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in records:
            date = parse_date_guess(rec.get("asOfDate") or rec.get("as_of_date") or rec.get("effectiveDate") or rec.get("date"))
            value = None
            for key in ("totalParValue", "parValue", "total", "value", "amount"):
                value = safe_float(rec.get(key))
                if value is not None:
                    break
            if date and value is not None:
                if abs(value) > 1_000_000_000:
                    value = value / 1_000_000_000.0
                elif abs(value) > 10_000:
                    value = value / 1_000.0
                parsed.append((date, value, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"raw_latest": parsed[-1][2]} if parsed else {}
        status = "ok" if latest else "unavailable"
        notes = "SOMA endpoint schema may change; use as weekly QT background" if latest else "Could not extract numeric SOMA summary from endpoint"
        return make_metric("SOMA", "SOMA holdings / QT background", "Fed负债端", latest, previous, "USD bn", "weekly", "NY Fed Markets API", url, status=status, notes=notes, extra=extra)
    except Exception as exc:
        return error_metric("SOMA", "SOMA holdings / QT background", "Fed负债端", "USD bn", "weekly", "NY Fed Markets API", url, exc)


def fetch_treasury_auctions(lookback_days: int) -> Metric:
    end = datetime.now(UTC).date()
    start = end - timedelta(days=lookback_days)
    params = urllib.parse.urlencode({"format": "json", "startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://www.treasurydirect.gov/TA_WS/securities/search?{params}"
    try:
        payload = http_get_json(url)
        records = payload if isinstance(payload, list) else payload.get("data", []) if isinstance(payload, dict) else []
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in records:
            if not isinstance(rec, dict):
                continue
            date = parse_date_guess(rec.get("auctionDate") or rec.get("auction_date"))
            value = safe_float(rec.get("bidToCoverRatio") or rec.get("bid_to_cover_ratio"))
            if date and value is not None:
                parsed.append((date, value, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"latest_auction": parsed[-1][2], "lookback_days": lookback_days} if parsed else {"lookback_days": lookback_days}
        notes = "Uses bid-to-cover as free auction demand proxy; auction tail requires WI yield not available here"
        status = "ok" if latest else "unavailable"
        return make_metric("UST_AUCTION_BTC", "Treasury auction bid-to-cover", "国债/抵押品", latest, previous, "ratio", "event-based", "TreasuryDirect", url, status=status, notes=notes, extra=extra)
    except Exception as exc:
        return error_metric("UST_AUCTION_BTC", "Treasury auction bid-to-cover", "国债/抵押品", "ratio", "event-based", "TreasuryDirect", url, exc)


def fetch_tbill_auction_metrics(lookback_days: int) -> List[Metric]:
    """Fetch T-bill auction size and demand as date-level aggregates."""
    end = datetime.now(UTC).date()
    start = end - timedelta(days=lookback_days)
    params = urllib.parse.urlencode({"format": "json", "startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://www.treasurydirect.gov/TA_WS/securities/search?{params}"
    category = "国债/抵押品"
    try:
        payload = http_get_json(url)
        records = payload if isinstance(payload, list) else payload.get("data", []) if isinstance(payload, dict) else []
        grouped: Dict[str, Dict[str, Any]] = {}
        for rec in records:
            if not isinstance(rec, dict):
                continue
            if str(rec.get("securityType", "")).lower() != "bill":
                continue
            date = parse_date_guess(rec.get("auctionDate") or rec.get("auction_date"))
            amount = fiscal_amount_to_bn(safe_float(rec.get("offeringAmount") or rec.get("offering_amount")))
            btc = safe_float(rec.get("bidToCoverRatio") or rec.get("bid_to_cover_ratio"))
            if not date or amount is None:
                continue
            bucket = grouped.setdefault(date, {"size": 0.0, "btc_weighted_sum": 0.0, "btc_weight": 0.0, "records": [], "terms": []})
            bucket["size"] += amount
            if btc is not None:
                bucket["btc_weighted_sum"] += btc * amount
                bucket["btc_weight"] += amount
            bucket["records"].append(rec)
            term = str(rec.get("securityTerm") or "").strip()
            if term:
                bucket["terms"].append(term)
        parsed: List[Tuple[str, float, Optional[float], Dict[str, Any]]] = []
        for date, bucket in grouped.items():
            btc_value = bucket["btc_weighted_sum"] / bucket["btc_weight"] if bucket["btc_weight"] else None
            parsed.append((date, bucket["size"], btc_value, bucket))
        parsed = sorted(parsed, key=lambda x: x[0])
        if not parsed:
            return [
                error_metric("TBILL_AUCTION_SIZE", "T-bill auction offering amount", category, "USD bn", "event-based", "TreasuryDirect", url, Exception("no T-bill auction data")),
                error_metric("TBILL_AUCTION_BTC", "T-bill auction bid-to-cover", category, "ratio", "event-based", "TreasuryDirect", url, Exception("no T-bill auction data")),
            ]
        latest = parsed[-1]
        previous = parsed[-2] if len(parsed) >= 2 else None
        latest_date, latest_size, latest_btc, latest_bucket = latest
        previous_size = (previous[0], previous[1]) if previous else None
        previous_btc = (previous[0], previous[2]) if previous and previous[2] is not None else None
        terms = ", ".join(sorted(set(latest_bucket.get("terms", []))))
        shared_extra = {"latest_auctions": latest_bucket.get("records", []), "terms": terms, "lookback_days": lookback_days}
        notes = f"Aggregates all Treasury Bill auctions on the latest auction date; bid-to-cover is offering-amount weighted. Latest terms: {terms or 'NA'}."
        size_metric = make_metric(
            "TBILL_AUCTION_SIZE",
            "T-bill auction offering amount",
            category,
            (latest_date, latest_size),
            previous_size,
            "USD bn",
            "event-based",
            "TreasuryDirect",
            url,
            notes=notes,
            extra=shared_extra,
        )
        btc_metric = make_metric(
            "TBILL_AUCTION_BTC",
            "T-bill auction bid-to-cover",
            category,
            (latest_date, latest_btc) if latest_btc is not None else None,
            previous_btc,
            "ratio",
            "event-based",
            "TreasuryDirect",
            url,
            status="ok" if latest_btc is not None else "unavailable",
            notes=notes,
            extra=shared_extra,
        )
        return [size_metric, btc_metric]
    except Exception as exc:
        return [
            error_metric("TBILL_AUCTION_SIZE", "T-bill auction offering amount", category, "USD bn", "event-based", "TreasuryDirect", url, exc),
            error_metric("TBILL_AUCTION_BTC", "T-bill auction bid-to-cover", category, "ratio", "event-based", "TreasuryDirect", url, exc),
        ]


def fetch_upcoming_auctions(lookforward_days: int = 60) -> Dict[str, Any]:
    """Fetch upcoming Treasury auction calendar and offering amounts from TreasuryDirect."""
    today = datetime.now(UTC).date()
    end = today + timedelta(days=lookforward_days)
    params = urllib.parse.urlencode({"format": "json", "startDate": today.isoformat(), "endDate": end.isoformat()})
    url = f"https://www.treasurydirect.gov/TA_WS/securities/search?{params}"
    try:
        payload = http_get_json(url)
        records = payload if isinstance(payload, list) else payload.get("data", []) if isinstance(payload, dict) else []
        auctions: List[Dict[str, Any]] = []
        for rec in records:
            if not isinstance(rec, dict):
                continue
            auction_date = parse_date_guess(rec.get("auctionDate") or rec.get("auction_date"))
            if not auction_date or auction_date < today.isoformat():
                continue
            security_type = str(rec.get("securityType") or rec.get("type") or "").strip()
            security_term = str(rec.get("securityTerm") or rec.get("term") or "").strip()
            raw_amount = rec.get("offeringAmount") or rec.get("offering_amount")
            amount_bn = fiscal_amount_to_bn(safe_float(raw_amount))
            is_bill = security_type.lower() == "bill"
            is_note_or_bond = security_type.lower() in {"note", "bond", "tips", "frn"}
            amount_text = f"${amount_bn:.0f}bn" if amount_bn is not None else "待公布"
            auctions.append({
                "auctionDate": auction_date,
                "issueDate": parse_date_guess(rec.get("issueDate") or rec.get("issue_date")) or "",
                "announcementDate": parse_date_guess(rec.get("announcementDate") or rec.get("announcement_date")) or "",
                "securityType": security_type,
                "securityTerm": security_term,
                "offeringAmount": amount_bn,
                "offeringAmountText": amount_text,
                "cusip": rec.get("cusip") or rec.get("CUSIP") or "",
                "is_bill": is_bill,
                "is_note_or_bond": is_note_or_bond,
            })
        auctions.sort(key=lambda item: (item.get("auctionDate") or "", item.get("securityType") or "", item.get("securityTerm") or ""))
        bill_auctions = [a for a in auctions if a.get("is_bill")]
        large_auctions = [a for a in auctions if (a.get("offeringAmount") or 0) >= 75]
        by_date: Dict[str, Dict[str, Any]] = {}
        for a in bill_auctions:
            date = a.get("auctionDate") or "NA"
            bucket = by_date.setdefault(date, {"auctionDate": date, "totalBillOffering": 0.0, "items": []})
            if a.get("offeringAmount") is not None:
                bucket["totalBillOffering"] += float(a["offeringAmount"])
            bucket["items"].append(a)
        bill_schedule = []
        for date in sorted(by_date):
            bucket = by_date[date]
            bucket["totalBillOfferingText"] = f"${bucket['totalBillOffering']:.0f}bn" if bucket["totalBillOffering"] else "待公布"
            bill_schedule.append(bucket)
        return {
            "status": "ok",
            "as_of": today.isoformat(),
            "lookforward_days": lookforward_days,
            "source_url": url,
            "auctions": auctions,
            "bill_schedule": bill_schedule,
            "next_auctions": auctions[:10],
            "large_auctions": large_auctions[:10],
            "notes": "TreasuryDirect future auction calendar. offeringAmount may be absent before official announcement; treat missing amounts as data risk, not zero issuance.",
        }
    except Exception as exc:
        return {
            "status": "error",
            "as_of": today.isoformat(),
            "lookforward_days": lookforward_days,
            "source_url": url,
            "auctions": [],
            "bill_schedule": [],
            "next_auctions": [],
            "large_auctions": [],
            "notes": str(exc),
        }


def fetch_ofr_series(mnemonic: str, metric_id: str, name: str) -> Metric:
    params = urllib.parse.urlencode({"mnemonic": mnemonic})
    url = f"https://data.financialresearch.gov/v1/series/timeseries?{params}"
    try:
        payload = http_get_json(url)
        parsed: List[Tuple[str, float]] = []
        if isinstance(payload, list):
            for row in payload:
                if isinstance(row, list) and len(row) >= 2:
                    date = parse_date_guess(row[0])
                    value = fiscal_amount_to_bn(safe_float(row[1]))
                    if date and value is not None:
                        parsed.append((date, value))
        else:
            records = list(walk_dicts(payload))
            for rec in records:
                date = parse_date_guess(rec.get("date") or rec.get("observation_date") or rec.get("time_period"))
                value = None
                for key in ("value", "obs_value", "amount"):
                    value = safe_float(rec.get(key))
                    if value is not None:
                        break
                value = fiscal_amount_to_bn(value)
                if date and value is not None:
                    parsed.append((date, value))
        parsed = sorted(set(parsed), key=lambda x: x[0])
        latest = parsed[-1] if parsed else None
        previous = parsed[-2] if len(parsed) >= 2 else None
        status = "ok" if latest else "unavailable"
        notes = "Optional OFR STFM series; if unavailable, do not block the main briefing"
        return make_metric(metric_id, name, "国债/抵押品", latest, previous, "USD bn", "weekly", "OFR STFM", url, status=status, notes=notes)
    except Exception as exc:
        metric = error_metric(metric_id, name, "国债/抵押品", "USD bn", "weekly", "OFR STFM", url, exc)
        metric.notes = f"Optional source failed: {metric.notes}"
        return metric


def add_synthetic_policy_anchor(metrics: List[Metric]) -> None:
    mm = metric_map(metrics)
    effr = mm.get("EFFR")
    if not effr or not effr.extra:
        return
    raw = effr.extra.get("raw_latest", {})
    prev_raw = {}
    anchor = safe_float(raw.get("targetRateTo"))
    if anchor is None:
        return
    metric = Metric(
        id="POLICY_UPPER_NYFED",
        name="Fed target upper bound from NY Fed EFFR record",
        category="政策锚",
        value=anchor,
        previous=anchor,
        change=0.0,
        unit="%",
        as_of=effr.as_of,
        previous_as_of=effr.previous_as_of,
        frequency="daily / policy step",
        source="NY Fed Markets API",
        source_url=effr.source_url,
        status="ok",
        notes="Fallback policy anchor when IORB/FRED is unavailable; not identical to IORB",
        stale_days=effr.stale_days,
        extra={"raw_latest": raw, "raw_previous": prev_raw},
    )
    metrics.append(metric)


def fetch_all_metrics(auction_lookback_days: int) -> List[Metric]:
    api_jobs = [
        lambda: fetch_nyfed_rate("sofr", "Secured Overnight Financing Rate", True),
        fetch_nyfed_sofr_volume,
        lambda: fetch_nyfed_rate("tgcr", "Tri-party General Collateral Rate", True),
        lambda: fetch_nyfed_rate("bgcr", "Broad General Collateral Rate", True),
        lambda: fetch_nyfed_rate("effr", "Effective Federal Funds Rate", False),
        lambda: fetch_nyfed_rate("obfr", "Overnight Bank Funding Rate", False),
        fetch_tga,
        lambda: fetch_nyfed_rrp(14),
        lambda: fetch_treasury_auctions(auction_lookback_days),
        fetch_soma_summary,
        lambda: fetch_ofr_series("NYPD-PD_AFtD_T-A", "REPO_FAILS_UST", "Primary dealer Treasury repo fails"),
    ]
    fred_jobs = [
        lambda: fetch_fred_series("IORB", "Interest on Reserve Balances", "政策锚", "%", "daily / policy step"),
        lambda: fetch_fred_series("WRESBAL", "Reserve balances with Federal Reserve Banks", "Fed负债端", "USD bn", "weekly"),
        lambda: fetch_fred_series("DTWEXBGS", "Trade-weighted broad dollar index", "离岸美元", "index", "daily T+1"),
        lambda: fetch_fred_series("DCPN3M", "90-day AA nonfinancial commercial paper", "信用传导", "%", "daily T+1"),
        lambda: fetch_fred_series("DFEDTARU", "Federal funds target range upper limit", "政策锚", "%", "daily / policy step"),
        lambda: fetch_fred_series("BAMLH0A0HYM2", "ICE BofA US High Yield OAS", "信用传导", "%", "daily T+1"),
        lambda: fetch_fred_series("BAMLC0A0CM", "ICE BofA US Corporate OAS", "信用传导", "%", "daily T+1"),
        lambda: fetch_fred_series("DTB3", "3-month Treasury bill secondary market rate", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS3MO", "3-month Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS1", "1-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS2", "2-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS3", "3-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS10", "10-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DFII10", "10-year Treasury inflation-indexed security real yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS30", "30-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("T10Y2Y", "10-year minus 2-year Treasury spread", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("T10Y3M", "10-year minus 3-month Treasury spread", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("VIXCLS", "CBOE Volatility Index: VIX", "证券市场风险偏好", "index", "daily T+1"),
        lambda: fetch_fred_series("NFCI", "Chicago Fed National Financial Conditions Index", "金融条件", "index", "weekly"),
    ]
    metrics: List[Metric] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_index = {executor.submit(job): index for index, job in enumerate(api_jobs)}
        for future in concurrent.futures.as_completed(future_to_index):
            try:
                metrics.append(future.result(timeout=1))
            except Exception as exc:
                index = future_to_index[future]
                metrics.append(error_metric(f"JOB_{index}", "Uncaught fetch job error", "系统", "", "unknown", "internal", "", exc))
    metrics.extend(fetch_tbill_auction_metrics(auction_lookback_days))
    for job in fred_jobs:
        metrics.append(job())
        time.sleep(0.15)
    add_synthetic_policy_anchor(metrics)
    metrics.sort(key=lambda m: (m.category, m.id))
    return metrics


def fetch_cftc_jpy_position() -> Dict[str, Any]:
    params = urllib.parse.urlencode({
        "cftc_contract_market_code": "097741",
        "$limit": 2,
        "$order": "report_date_as_yyyy_mm_dd DESC",
    })
    url = f"https://publicreporting.cftc.gov/resource/6dca-aqww.json?{params}"
    try:
        payload = http_get_json(url, timeout=12, retries=1)
        records = payload if isinstance(payload, list) else []
        latest = records[0] if records else {}
        previous = records[1] if len(records) > 1 else {}
        long_pos = safe_float(latest.get("noncomm_positions_long_all"))
        short_pos = safe_float(latest.get("noncomm_positions_short_all"))
        open_interest = safe_float(latest.get("open_interest_all"))
        prev_long = safe_float(previous.get("noncomm_positions_long_all"))
        prev_short = safe_float(previous.get("noncomm_positions_short_all"))
        net = (long_pos - short_pos) if long_pos is not None and short_pos is not None else None
        prev_net = (prev_long - prev_short) if prev_long is not None and prev_short is not None else None
        crowded_ratio = (net / open_interest) if net is not None and open_interest else None
        return {
            "status": "ok" if net is not None else "unavailable",
            "as_of": parse_date_guess(latest.get("report_date_as_yyyy_mm_dd")),
            "value": net,
            "previous": prev_net,
            "change": (net - prev_net) if net is not None and prev_net is not None else None,
            "crowded_ratio": crowded_ratio,
            "source_url": url,
            "notes": "CFTC non-commercial JPY futures positioning; negative net means speculative JPY shorts crowded.",
        }
    except Exception as exc:
        return {
            "status": "error",
            "as_of": None,
            "value": None,
            "previous": None,
            "change": None,
            "crowded_ratio": None,
            "source_url": url,
            "notes": str(exc),
        }
