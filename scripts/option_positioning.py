"""CFTC S&P 500 Consolidated TFF dealer positioning in futures-equivalent contracts."""
from __future__ import annotations

import re
from time import monotonic
from datetime import date, timedelta
from urllib.parse import urlencode

from .utils import http_get_json, now_bjt


MARKET_CODE = "13874+"
SERIES_ID = "SP500_CFTC_DEALER_OPTION_DELTA_EQUIV"
DATASETS = {"combined": ("yw9f-hn96", "Combined"), "futures_only": ("gpe5-46if", "FutOnly")}
_PAGE_SIZE = 1000
_FIELDS = ("id", "report_date_as_yyyy_mm_dd", "cftc_contract_market_code", "contract_market_name",
           "market_and_exchange_names", "futonly_or_combined", "contract_units", "open_interest_all",
           "dealer_positions_long_all", "dealer_positions_short_all", "dealer_positions_spread_all")
_DATE = "report_date_as_yyyy_mm_dd"


def _day(stamp):
    raw = str(stamp)
    if len(raw) > 10 and raw[10] not in ("T", " "):
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def _capture_source(kind, cutoff):
    started = monotonic()
    dataset, _ = DATASETS[kind]
    url = f"https://publicreporting.cftc.gov/resource/{dataset}.json"
    where = f"cftc_contract_market_code='{MARKET_CODE}' AND {_DATE} <= '{cutoff.isoformat()}T23:59:59.999'"
    result = {"dataset_id": dataset, "market_code": MARKET_CODE, "source_url": url,
              "where": where, "selected_fields": list(_FIELDS), "rows": [], "status": "error"}
    rows = result["rows"]
    try:
        count_query = urlencode({"$select": "count(*) as observations", "$where": where})
        count = http_get_json(f"{url}?{count_query}", timeout=15, retries=1)
        expected = int(count[0]["observations"])
        if expected < 0:
            raise ValueError("Invalid CFTC row count")
        result["expected_observations"] = expected
        # The count bounds the loop. Key order checks also catch ignored offsets.
        while len(rows) < expected:
            query = urlencode({"$select": ",".join(_FIELDS), "$where": where,
                               "$order": f"{_DATE} ASC,id ASC", "$limit": _PAGE_SIZE, "$offset": len(rows)})
            page = http_get_json(f"{url}?{query}", timeout=15, retries=1)
            if not isinstance(page, list) or not page or any(not isinstance(row, dict) for row in page):
                raise ValueError("CFTC returned an empty or invalid page before the advertised count")
            if len(rows) + len(page) > expected:
                raise ValueError("CFTC count changed during capture")
            keys = [(str(row.get(_DATE) or ""), str(row.get("id") or "")) for row in page]
            if keys != sorted(keys) or (rows and keys[0] <= (str(rows[-1].get(_DATE)), str(rows[-1].get("id")))):
                raise ValueError("CFTC pagination produced repeated or out-of-order rows")
            rows.extend(page)
        result["status"] = "ok" if rows else "missing"
    except (KeyError, IndexError, OSError, RuntimeError, ValueError, TypeError) as exc:
        result["error"] = str(exc)[:500]
    result.update(captured_at_bjt=now_bjt().isoformat(), captured_observations=len(rows), seconds=round(monotonic() - started, 3))
    return result


def capture_positioning(stamp):
    """Retrieve both independently identified public TFF reports and retain their raw selected fields."""
    cutoff = _day(stamp)
    if not cutoff:
        raise ValueError("A valid frozen observation cutoff is required")
    sources = {kind: _capture_source(kind, cutoff) for kind in DATASETS}
    status = next((s["status"] for s in sources.values() if s["status"] != "ok"), "ok")
    return {"generated_at_bjt": str(stamp), "market_code": MARKET_CODE, "sources": sources, "status": status}


def _contracts(value):
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    if isinstance(value, str) and re.fullmatch(r"\d+", value.strip()):
        return int(value)
    return None


def _report_rows(source, kind, cutoff):
    valid, excluded, future, undated = {}, set(), set(), 0
    week_dates, fingerprints = {}, {}
    market_type = DATASETS[kind][1]
    for row in source.get("rows") or []:
        day = _day(row.get(_DATE)) if isinstance(row, dict) else None
        if not day:
            undated += 1
            continue
        if day > cutoff:
            future.add(day)
            continue
        week = day - timedelta(days=day.weekday())
        if week in week_dates and week_dates[week] != day:
            excluded.update((day, week_dates[week]))
        else:
            week_dates[week] = day
        long = _contracts(row.get("dealer_positions_long_all"))
        short = _contracts(row.get("dealer_positions_short_all"))
        unit = str(row.get("contract_units") or "").strip(" '").upper()
        match = re.fullmatch(r"\(S&P 500 INDEX X \$(\d+(?:\.\d+)?)\)", unit)
        if (row.get("cftc_contract_market_code") != MARKET_CODE or row.get("futonly_or_combined") != market_type
                or not match or long is None or short is None):
            excluded.add(day)
            continue
        multiplier = float(match.group(1))
        if multiplier <= 0:
            excluded.add(day)
            continue
        values = (long, short, multiplier)
        fingerprint = (values, row.get("id"), row.get("contract_market_name"), row.get("market_and_exchange_names"),
                       row.get("open_interest_all"), row.get("dealer_positions_spread_all"))
        if day in fingerprints and fingerprints[day] != fingerprint:
            excluded.add(day)
        else:
            fingerprints[day] = fingerprint
            valid[day] = values
    for day in excluded:
        valid.pop(day, None)
    return valid, {"invalid_or_conflicting_dates": sorted(d.isoformat() for d in excluded),
                   "after_cutoff_dates": sorted(d.isoformat() for d in future), "undated_rows": undated}


def build_positioning_history(capture, stamp):
    """Replay only captured rows. A report week is dated by its positions, not by release."""
    cutoff = _day(stamp)
    if not cutoff:
        raise ValueError("A valid frozen observation cutoff is required")
    sources = (capture or {}).get("sources") or {}
    data, audits, statuses, captures, messages = {}, {}, {}, {}, []
    for kind, (expected_id, _) in DATASETS.items():
        source = sources.get(kind) or {}
        status = source.get("status") or "missing"
        if source and (source.get("dataset_id") != expected_id or source.get("market_code") != MARKET_CODE):
            status, source = "source_mismatch", {}
        data[kind], audits[kind] = _report_rows(source, kind, cutoff)
        statuses[kind], captures[kind] = status, source.get("captured_at_bjt")
        if status != "ok":
            messages.append(f"{kind}: {source.get('error') or status}")
    combined, futures = data["combined"], data["futures_only"]
    points, incompatible, transitions = [], [], []
    previous_week = previous_multiplier = previous_value = None
    for day in sorted(combined.keys() & futures.keys()):
        cl, cs, multiplier = combined[day]
        fl, fs, future_multiplier = futures[day]
        if multiplier != future_multiplier:
            incompatible.append(day.isoformat())
            continue
        combined_net, futures_net = cl - cs, fl - fs
        value = combined_net - futures_net
        week = day - timedelta(days=day.weekday())
        same_unit = multiplier == previous_multiplier
        consecutive = previous_week is not None and week - previous_week == timedelta(days=7)
        if previous_multiplier is not None and not same_unit:
            transitions.append(day.isoformat())
        points.append({"date": day.isoformat(), "value": value, "combined_net": combined_net,
                       "futures_only_net": futures_net, "combined_long": cl, "combined_short": cs,
                       "futures_only_long": fl, "futures_only_short": fs, "contract_multiplier": multiplier,
                       "change": value - previous_value if same_unit and consecutive else None})
        previous_week, previous_multiplier, previous_value = week, multiplier, value
    all_days = combined.keys() | futures.keys()
    for audit in audits.values():
        all_days.update(date.fromisoformat(day) for day in audit["invalid_or_conflicting_dates"])
    weeks = {day - timedelta(days=day.weekday()) for day in all_days}
    missing_weeks = []
    if weeks:
        first, last = min(weeks), max(weeks)
        missing_weeks = [(first + timedelta(weeks=i)).isoformat() for i in range((last - first).days // 7 + 1)
                         if first + timedelta(weeks=i) not in weeks]
    latest = date.fromisoformat(points[-1]["date"]) if points else None
    age = (cutoff - latest).days if latest else None
    source_status = next((s for s in statuses.values() if s != "ok"), "ok")
    status = source_status
    if source_status == "ok":
        if not latest:
            status = "missing"
        elif age > 14:
            status = "stale"
        elif latest < max(all_days):
            status = "partial_latest"
    source_histories = {kind: [{"date": day.isoformat(), "dealer_long": long, "dealer_short": short,
                                 "contract_multiplier": multiplier} for day, (long, short, multiplier) in sorted(rows.items())]
                        for kind, rows in data.items()}
    return {
        "series_id": SERIES_ID, "status": status, "source_status": source_status, "source_statuses": statuses,
        "source_captured_at_bjt": captures, "as_of": latest.isoformat() if latest else None, "stale_days": age,
        "points": points, "source_histories": source_histories, "message": "；".join(messages),
        "coverage": {"cutoff": cutoff.isoformat(), "observations": len(points), "source_gaps": audits,
                     "missing_combined_dates": sorted(day.isoformat() for day in futures.keys() - combined.keys()),
                     "missing_futures_only_dates": sorted(day.isoformat() for day in combined.keys() - futures.keys()),
                     "missing_both_week_starts": missing_weeks, "incompatible_unit_dates": incompatible,
                     "unit_change_dates": transitions},
        "interpretation": "CME标普500合并市场的交易商/中介分类，每周联合报告净多空减纯期货报告净多空，表示期权部分按交易所Delta折算的净期货等值手数。正负号描述报告内的方向。",
        "limitations": "周度仓位快照不能识别逐合约Gamma、盘中对冲交易或场外仓位。观测日期早于公开发布时间。历史修订记录反映本次冻结版本。",
    }
