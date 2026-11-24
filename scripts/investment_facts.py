"""Auditable medium-horizon facts; factual calculations never assign investment scores.

``enrich_package`` is entirely offline.  Market downloads are isolated in
``build_market_context`` and use the project's existing bounded HTTP helper.
Windows count valid observations, not calendar/trading days.  Historical source
downloads are not point-in-time vintages and must not be used as such in a test.
"""
from __future__ import annotations

import csv
import io
import json
import math
import re
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode

from .investment_review import _timestamp
from .utils import BJT, http_get_text

WINDOWS = (5, 20, 60)
MARKET_SERIES = {
    "SP500": {"name": "标普500价格指数", "unit": "index", "frequency": "daily close / US trading observations",
              "source_note": "S&P Dow Jones Indices via FRED；收盘价格指数，不含股息。"},
    "NASDAQCOM": {"name": "纳斯达克综合价格指数", "unit": "index", "frequency": "daily close / US trading observations",
                  "source_note": "Nasdaq via FRED；纳斯达克综合指数，不是纳斯达克100。"},
    "CBBTCUSD": {"name": "Coinbase比特币美元价格", "unit": "USD", "frequency": "daily / 7-day observations",
                 "source_note": "Coinbase via FRED；源标注每日5 PM PST，含周末，不是美股交易日口径。"},
}
CORE_IDS = {
    "SOFR", "EFFR", "OBFR", "TGCR", "BGCR", "SOFR_VOLUME", "SRP_ACCEPTED",
    "IORB", "RRPONTSYD", "TGA", "SOMA", "WRESBAL", "DGS1", "DGS2", "DGS3",
    "DGS5", "DGS7", "DGS10", "DFII5", "DFII7", "DFII10", "DTWEXBGS",
    "BAMLH0A0HYM2", "BAMLC0A0CM", "VIXCLS", "NFCI",
    "FRBSF_EXPECTED_SHORT_2Y", "FRBSF_EXPECTED_SHORT_10Y", "FRBSF_TERM_PREMIUM_10Y",
}
CONFIRMATION_IDS = {"VIXCLS", "BAMLH0A0HYM2", "BAMLC0A0CM", "NFCI", "DTWEXBGS"}
MONEY_IDS = {"RRPONTSYD", "TGA", "SOMA", "WRESBAL"}


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if math.isfinite(value) else None


def _day(value):
    try:
        return date.fromisoformat(str(value)[:10]).isoformat()
    except (TypeError, ValueError):
        return None


def _points(rows, cutoff, *, source=None, unit=None):
    """Reject contradictory duplicates rather than selecting one arbitrarily."""
    by_date, conflicts = {}, set()
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        d, v = _day(row.get("date") or row.get("as_of")), _number(row.get("value"))
        if not d or d > cutoff or v is None:
            continue
        if source and row.get("source") and row["source"] != source:
            continue
        if unit and row.get("unit") and row["unit"] != unit:
            continue
        if d in by_date and not math.isclose(by_date[d], v, abs_tol=1e-9, rel_tol=1e-9):
            conflicts.add(d)
        by_date[d] = v
    return [(d, v) for d, v in sorted(by_date.items()) if d not in conflicts]


def _metric_rows(canonical, snapshot, cutoff):
    """Only use the raw row actually selected by canonical source/date/value."""
    mid = str(canonical.get("id", "")).upper()
    source, unit = canonical.get("source"), canonical.get("unit")
    reported = canonical.get("reported_future_endpoint", canonical)
    end, value = _day(reported.get("as_of")), _number(reported.get("value"))
    future_policy_rate = mid == "IORB" and end and end > cutoff
    if not end or (end > cutoff and not future_policy_rate) or value is None or reported.get("status") not in (None, "ok", "stale"):
        return [], "canonical_unusable"
    candidates = [r for r in snapshot.get("metrics", []) if isinstance(r, dict)
                  and str(r.get("id", "")).upper() == mid
                  and r.get("source") == source and r.get("unit") == unit
                  and _day(r.get("as_of")) == end and _number(r.get("value")) == value]
    if not candidates:
        return [], "canonical_source_history_missing"
    # Equivalent copies are harmless; contradictory histories are never merged.
    row = max(candidates, key=lambda r: len((r.get("extra") or {}).get("history") or []))
    rows = _points((row.get("extra") or {}).get("history"), min(cutoff, end), source=source, unit=unit)
    if not rows:
        return [], "history_missing"
    if not future_policy_rate and (rows[-1][0] != end or not math.isclose(rows[-1][1], value, abs_tol=1e-8, rel_tol=1e-9)):
        return [], "history_endpoint_mismatch"
    return rows, "ok"


def _effective_policy_rate(row, points, cutoff):
    """Keep the published future effective date separate from the in-force rate."""
    reported = row.get("reported_future_endpoint", row)
    if not _day(reported.get("as_of")) or _day(reported["as_of"]) <= cutoff:
        return
    row["reported_future_endpoint"] = {key: reported.get(key) for key in ("as_of", "value", "status")}
    end, value = points[-1] if points else (None, None)
    start, previous = points[-2] if len(points) > 1 else (None, None)
    history = {"observations": len(points), "basis": "valid observations through capture date"}
    for n in WINDOWS:
        if len(points) > n:
            history[str(n)] = {"start": points[-n-1][0], "end": end, "change": value - points[-n-1][1]}
    source_status = reported.get("status") or "ok"
    row.update(value=value, as_of=end, previous=previous, previous_as_of=start,
               change=value - previous if previous is not None else None,
               history_summary=history, distribution={},
               status=source_status if points or source_status not in ("ok", "stale") else "missing")
    row["status"], row["stale_days"] = _freshness(row, cutoff)
    row["source_selection"] = {**(row.get("source_selection") or {}),
                               "reason": f"{row.get('source')} 截至 {cutoff} 的最近有效观测日期为 {end or '未知'}。"}


def _frequency_label(frequency):
    value = str(frequency).lower()
    if "weekly" in value or "周" in value:
        return "周频"
    if "monthly" in value or "月" in value:
        return "月频"
    if "daily" in value or "日" in value:
        return "日频"
    return None


def _freshness(row, cutoff):
    """Preserve source errors and separately account for observation age."""
    source_status = row.get("status")
    d = _day(row.get("as_of"))
    age = (date.fromisoformat(cutoff) - date.fromisoformat(d)).days if d else None
    label = _frequency_label(row.get("frequency"))
    limit = 14 if label == "周频" else 62 if label == "月频" else 5
    if source_status not in ("ok", "stale"):
        return source_status or "unknown_source_status", age
    if source_status == "stale" or age is None or age < 0 or age > limit:
        return "stale", age
    return "ok", age


def _role(mid):
    if mid in CONFIRMATION_IDS:
        return "market_confirmation"
    if mid in MONEY_IDS:
        return "money_supply"
    if mid == "IORB":
        return "policy_anchor"
    if mid.startswith(("DGS", "DFII", "FRBSF_")):
        return "asset_pricing"
    return "funding_price"


def _window_facts(mid, name, rows, unit, frequency, source, base_ids, *, prefix="trend", role=None, returns=False):
    result = []
    freq_label = _frequency_label(frequency)
    if not rows or not freq_label:
        return result
    for n in WINDOWS:
        if len(rows) <= n:
            continue
        start, end = rows[-n-1], rows[-1]
        if returns and start[1] <= 0:
            continue
        value = (end[1] / start[1] - 1) * 100 if returns else end[1]
        change = value if returns else end[1] - start[1]
        result.append({
            "fact_id": f"{prefix}:{mid}:{n}obs", "id": mid,
            "name": f"{name}：{n}个有效{freq_label}观测间隔" + ("价格收益率" if returns else "变化"),
            "value": value, "previous": 0.0 if returns else start[1], "change": change,
            "unit": "%" if returns else unit, "change_unit": "percentage points" if unit == "%" and not returns else "%" if returns else unit,
            "as_of": end[0], "previous_as_of": start[0], "frequency": frequency,
            "source": source, "status": "ok", "base_fact_ids": base_ids,
            "window_observations": n, "window_start": start[0], "window_end": end[0],
            "window_label": f"{n}个有效{freq_label}观测间隔",
            "calendar_days": (date.fromisoformat(end[0]) - date.fromisoformat(start[0])).days,
            "role": role or _role(mid), "measurement": "price_return" if returns else "level_change",
            "vintage_status": "captured_history_not_verified_point_in_time",
        })
    return result


def _coverage(fid, message, *, as_of=None, status="missing", base_ids=None, **extra):
    return {"fact_id": f"coverage:{fid}", "id": fid, "name": message, "message": message,
            "value": None, "previous": None, "change": None, "unit": "coverage", "as_of": as_of,
            "frequency": "availability", "source": "captured input coverage audit", "status": status,
            "base_fact_ids": base_ids or [], **extra}


def _auction_key(row):
    auction_day, cusip = _day(row.get("auction_date")), row.get("cusip")
    if auction_day and cusip:
        return auction_day, cusip
    if auction_day and row.get("security_type") and row.get("security_term"):
        return auction_day, row["security_type"], row["security_term"]
    return row.get("fact_id")


def _capture_time(snapshot_file, ingested_at):
    stamp = re.search(r"(\d{8})_(\d{6})\.json$", snapshot_file or "")
    if stamp:
        return datetime.strptime("".join(stamp.groups()), "%Y%m%d%H%M%S").isoformat(sep=" ")
    return (ingested_at or "")[:19].replace("T", " ")


def _archived_auctions(history_db, generated_at):
    """Replay successful calendars in capture order, including withdrawals and amendments."""
    if history_db is None or not Path(history_db).is_file():
        return {}, False
    cutoff = _day(generated_at)
    timestamp = str(generated_at)[:19].replace("T", " ")
    captures = {}
    with closing(sqlite3.connect(Path(history_db).resolve().as_uri() + "?mode=ro", uri=True)) as db:
        db.row_factory = sqlite3.Row
        if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='treasury_auctions_ts'").fetchone():
            return {}, False
        for row in db.execute("""
            SELECT snapshot_file, ingested_at, calendar_as_of, auction_date, issue_date,
                   announcement_date, security_type, security_term, cusip, offering_amount_bn, source_url
            FROM treasury_auctions_ts WHERE status='ok' AND calendar_as_of <= ?
        """, (cutoff,)):
            captured = _capture_time(row["snapshot_file"], row["ingested_at"])
            calendar_day = _day(row["calendar_as_of"])
            if not calendar_day or not _day(captured) or captured > timestamp:
                continue
            captures.setdefault((captured, row["snapshot_file"], calendar_day), []).append(row)
    events = {}
    for (captured, filename, calendar_day), rows in sorted(captures.items()):
        # A later successful calendar replaces all previously listed upcoming auctions.
        events = {k: r for k, r in events.items() if r["auction_date"] < calendar_day}
        for row in rows:
            event = {k: row[k] for k in ("auction_date", "issue_date", "announcement_date", "security_type", "security_term", "cusip", "source_url")}
            key = _auction_key(event)
            if key is None:
                continue
            if not event["issue_date"] or event["issue_date"] < cutoff:
                events.pop(key, None)
                continue
            event.update(fact_id="event:settlement:" + ":".join(key),
                         event_type="treasury_auction_announcement", source="TreasuryDirect",
                         gross_announced_offering_usd_bn=row["offering_amount_bn"],
                         maturities_usd_bn=None, net_cash_impact_usd_bn=None,
                         captured_at_bjt=captured, capture_file=filename)
            events[key] = event
    return events, bool(captures)


def _settlement_sources(event_facts, snapshot, previous_package, history_db, generated_at):
    cutoff = _day(generated_at)
    source = snapshot.get("upcoming_auctions") or {}
    calendar_day = _day(source.get("as_of") or event_facts.get("as_of")) or cutoff
    raw_announcements = {
        _auction_key({"auction_date": a.get("auctionDate"), "cusip": a.get("cusip"),
                      "security_type": a.get("securityType"), "security_term": a.get("securityTerm")}): a.get("announcementDate")
        for a in source.get("auctions", []) if isinstance(a, dict)
    }
    fresh = event_facts.get("upcoming_auctions") or []
    for row in fresh:
        if isinstance(row, dict) and not row.get("announcement_date"):
            row["announcement_date"] = raw_announcements.get(_auction_key(row))
    events, has_archive = _archived_auctions(history_db, generated_at)
    if not has_archive and previous_package and str(previous_package.get("generated_at_bjt") or "") <= str(generated_at):
        prior = previous_package.get("data", {}).get("facts", {}).get("event_facts") or {}
        for row in (prior.get("previously_announced_settlements") or []) + (prior.get("upcoming_auctions") or []):
            if isinstance(row, dict) and _auction_key(row):
                events[_auction_key(row)] = {**row, "captured_at_bjt": row.get("captured_at_bjt") or previous_package.get("generated_at_bjt")}
    current_keys = {_auction_key(r) for r in fresh if isinstance(r, dict)}
    success = event_facts.get("status") == "ok"
    last_day = (date.fromisoformat(cutoff) + timedelta(days=83)).isoformat()
    historical = []
    for key, row in events.items():
        issue, auction, announced = _day(row.get("issue_date")), _day(row.get("auction_date")), _day(row.get("announcement_date"))
        if (key in current_keys or not issue or not cutoff <= issue <= last_day
                or (announced and announced > cutoff) or (success and (not auction or auction >= calendar_day))):
            continue
        historical.append(row)
    event_facts["previously_announced_settlements"] = sorted(historical, key=lambda r: (r["issue_date"], r["fact_id"]))
    return source.get("status") or event_facts.get("status", "missing")


def _calendar(event_facts, cutoff, source_status):
    archived = event_facts.get("previously_announced_settlements") or []
    source_rows = (event_facts.get("upcoming_auctions") or []) + archived
    usable, seen = [], set()
    for i, row in enumerate(source_rows):
        if not isinstance(row, dict):
            continue
        issue, announced = _day(row.get("issue_date")), _day(row.get("announcement_date"))
        if not issue or issue < cutoff or (announced and announced > cutoff):
            continue
        key = _auction_key(row) or i
        if key in seen:
            continue
        seen.add(key)
        usable.append(row)
    results = []
    for days in (7, 28, 84):
        end = (date.fromisoformat(cutoff) + timedelta(days=days - 1)).isoformat()
        rows = [r for r in usable if _day(r.get("issue_date")) <= end]
        gross = [_number(r.get("gross_announced_offering_usd_bn")) for r in rows]
        maturity = [_number(r.get("maturities_usd_bn")) for r in rows]
        cash = [_number(r.get("net_cash_impact_usd_bn")) for r in rows]
        known_gross = [v for v in gross if v is not None and v >= 0]
        all_gross = bool(rows) and len(known_gross) == len(rows)
        # Even a populated schedule contains announced amounts only, not all future issuance.
        status = "partial_announced" if rows else "missing"
        if rows and source_status != "ok":
            status = "historical_after_source_failure"
        amount = sum(known_gross) if known_gross else None
        results.append({
            "fact_id": f"calendar:{days}d", "id": f"ANNOUNCED_SETTLEMENTS_{days}D",
            "name": f"未来{days}日已公告结算毛发行（含快照日）", "value": amount,
            "previous": None, "change": None, "unit": "USD bn", "as_of": cutoff,
            "frequency": "announced event schedule", "source": "TreasuryDirect",
            "source_url": event_facts.get("source_url") or next((r["source_url"] for r in rows if r.get("source_url")), None),
            "status": status, "source_status": source_status,
            "window_days": days, "window_start": cutoff, "window_end": end,
            "event_count": len(rows), "previously_captured_count": sum(r in archived for r in rows),
            "unknown_amount_count": len(gross) - len(known_gross),
            "gross_announced_offering_usd_bn": amount,
            "gross_amounts_complete_for_listed_events": all_gross,
            "maturities_usd_bn": sum(maturity) if rows and all(v is not None and v >= 0 for v in maturity) else None,
            "net_cash_impact_usd_bn": sum(cash) if rows and all(v is not None for v in cash) else None,
            "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation",
            "base_fact_ids": [r["fact_id"] for r in rows if r.get("fact_id")],
            "role": "announced_future_supply",
            "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。",
        })
    return results


def build_market_context(generated_at_bjt: str, fetch: bool = True, previous_context: dict | None = None) -> dict:
    """Capture public FRED price history without API keys or fabricated fallback.

    On fetch failure cached rows remain labelled cached_after_fetch_failure, with
    their original capture timestamp and latest observation, never fresh/ok.
    A successful refresh retains same-source earlier captures and overwrites
    matching dates with the downloaded values. Each row keeps its capture time.
    This function never writes; the pipeline owns the isolated output directory.
    ``fetch=False`` never contacts a source.
    """
    cutoff = _day(generated_at_bjt)
    if not cutoff:
        raise ValueError("generated_at_bjt must begin with an ISO date")
    now = datetime.now(BJT).isoformat()
    result = {"generated_at_bjt": generated_at_bjt, "retrieved_at_bjt": now if fetch else None,
              "price_history": {}, "series": {}, "role": "market_confirmation",
              "vintage_note": "下载历史为当前可得版本；保存本次可见快照，不证明历史数据在过去已发布。"}
    previous_context = previous_context or {}
    since = "1900-01-01"
    for sid, definition in MARKET_SERIES.items():
        info = {**definition, "source": "FRED public CSV", "source_url": f"https://fred.stlouisfed.org/series/{sid}",
                "requested_start": since, "requested_end": cutoff}
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?" + urlencode({"id": sid, "cosd": since, "coed": cutoff})
        rows, error = [], None
        old_info = previous_context.get("series", {}).get(sid, {})
        same_source = old_info.get("source") == "FRED public CSV" and old_info.get("source_url") in (None, info["source_url"])
        old_rows = previous_context.get("price_history", {}).get(sid, []) if same_source else []
        old_points = _points(old_rows, cutoff)
        captures = {str(r.get("date")): r.get("captured_at_bjt") or old_info.get("captured_at_bjt")
                    for r in old_rows if isinstance(r, dict)}
        if fetch:
            try:
                for row in csv.DictReader(io.StringIO(http_get_text(url, timeout=12, retries=0))):
                    try:
                        value = float(row.get(sid, ""))
                    except (TypeError, ValueError):
                        continue
                    rows.append({"date": row.get("observation_date") or row.get("DATE") or row.get("date"), "value": value})
                fresh_points = _points(rows, cutoff)
                if not fresh_points or any(v <= 0 for _, v in fresh_points):
                    raise ValueError("No valid positive price history returned")
                retained = [(d, v) for d, v in old_points if d < fresh_points[0][0] and v > 0]
                merged = dict(retained)
                merged.update(dict(fresh_points))
                points = sorted(merged.items())
                for d, _ in fresh_points:
                    captures[d] = now
                info.update(status="ok", captured_at_bjt=now, download_url=url,
                            refreshed_observations=len(fresh_points), refreshed_start=fresh_points[0][0],
                            refreshed_end=fresh_points[-1][0], retained_earlier_observations=len(retained),
                            retained_history_note="较早同源价格沿用先前捕获版本；仅本次下载窗口重新确认，每条价格保留capture时间。")
            except Exception as exc:
                error = str(exc)[:400]
                points = old_points
                info.update(status="cached_after_fetch_failure" if points else "missing", error=error,
                            captured_at_bjt=old_info.get("captured_at_bjt"), download_url=url)
        else:
            points = old_points
            info.update(status="cached_offline" if points else "missing", captured_at_bjt=old_info.get("captured_at_bjt"))
        info.update(observations=len(points), as_of=points[-1][0] if points else None,
                    stale_days=(date.fromisoformat(cutoff) - date.fromisoformat(points[-1][0])).days if points else None)
        result["series"][sid] = info
        result["price_history"][sid] = [{"date": d, "value": v, "captured_at_bjt": captures.get(d)} for d, v in points]
    return result


def _comparison_fact(mid, current, old, cutoff, previous_cutoff, previous_time):
    value, before = _number(current.get("value")), _number(old.get("value"))
    end, start = _day(current.get("as_of")), _day(old.get("as_of"))
    if value is None or before is None or not end or not start or start > end or end > cutoff or start > previous_cutoff:
        return None
    current_status, current_age = _freshness(current, cutoff)
    old_status, old_age = _freshness(old, previous_cutoff)
    return {
        "fact_id": f"comparison:{mid}", "id": mid, "name": f"{current.get('name', mid)}较上次成功事实包",
        "value": value, "previous": before, "change": value - before, "unit": current.get("unit"),
        "as_of": end, "previous_as_of": start, "frequency": "since previous captured package",
        "source": current.get("source"), "source_url": current.get("source_url"),
        "status": current_status if current_status != "ok" else old_status,
        "base_fact_ids": [current.get("fact_id", f"metric:{mid}")],
        "source_status": current.get("source_status", current.get("status")),
        "previous_source_status": old.get("source_status", old.get("status")),
        "stale_days": current_age, "previous_stale_days_at_capture": old_age,
        "role": current.get("role") or _role(mid), "previous_package_generated_at_bjt": previous_time,
        "comparison_kind": "revision_same_observation_date" if end == start and value != before else "unchanged" if end == start else "new_observation",
    }


def option_package_comparisons(options, previous_package, generated_at):
    """Compare published option readings, independently of their source-day or source-week change."""
    if not previous_package:
        return []
    previous_time = previous_package.get("generated_at_bjt")
    try:
        earlier = _timestamp(previous_time).astimezone(BJT)
        current_time = _timestamp(generated_at).astimezone(BJT)
    except ValueError:
        return []
    if earlier >= current_time:
        return []
    previous = previous_package.get("data", {}).get("facts", {}).get("investment", {}).get("options", {})
    pairs = (("volatility_spread", "iv_minus_rv21"), ("open_interest_share", "option_oi_share"))
    identity = ("fact_id", "measurement", "unit", "source", "source_url")
    comparisons = []
    for slot, mid in pairs:
        current, old = options.get(slot), previous.get(slot)
        if not isinstance(current, dict) or not isinstance(old, dict):
            continue
        if any(not current.get(key) or current[key] != old.get(key) for key in identity):
            continue
        multiplier = current.get("contract_multiplier")
        if multiplier is not None or old.get("contract_multiplier") is not None:
            if _number(multiplier) is None or multiplier <= 0 or _number(old.get("contract_multiplier")) != multiplier:
                continue
        row = _comparison_fact(mid, current, old, current_time.date().isoformat(), earlier.date().isoformat(), previous_time)
        if row:
            comparisons.append(row)
    return comparisons


def _package_comparisons(canonical, market_facts, previous_package, previous_snapshot, generated_at):
    previous_time = previous_package.get("generated_at_bjt")
    previous_cutoff = _day(previous_time)
    cutoff = _day(generated_at)
    if not previous_cutoff or str(previous_time)[:19].replace("T", " ") > str(generated_at)[:19].replace("T", " "):
        return []
    previous_facts = previous_package.get("data", {}).get("facts", {})
    previous = {r["id"]: r for r in previous_facts.get("canonical_metrics", []) if isinstance(r, dict) and r.get("id")}
    current_rows = [r for mid, r in canonical.items() if mid in CORE_IDS]
    for row in previous_facts.get("investment", {}).get("market_facts", []):
        if row.get("fact_id") == f"market:{row.get('id')}:level":
            previous[row["id"]] = row
    current_rows.extend(r for r in market_facts if r["fact_id"] == f"market:{r['id']}:level")
    comparisons = []
    for current in current_rows:
        mid = current["id"]
        old = previous.get(mid)
        if not old or current.get("source") != old.get("source") or current.get("unit") != old.get("unit"):
            continue
        if mid in MARKET_SERIES and current.get("source_url") != old.get("source_url"):
            continue
        if mid == "IORB" and (_day(old.get("as_of")) or "") > previous_cutoff:
            # Pre-3.1 captures stored the last published policy date, including future effective dates.
            if isinstance(previous_snapshot, (Path, str)) and Path(previous_snapshot).is_file():
                previous_snapshot = json.loads(Path(previous_snapshot).read_text(encoding="utf-8-sig"))
            if not isinstance(previous_snapshot, dict) or (previous_snapshot.get("generated_at_bjt") and previous_snapshot["generated_at_bjt"] != previous_time):
                continue
            old = dict(old)
            points, _ = _metric_rows(old, previous_snapshot, previous_cutoff)
            _effective_policy_rate(old, points, previous_cutoff)
        row = _comparison_fact(mid, current, old, cutoff, previous_cutoff, previous_time)
        if row:
            comparisons.append(row)
    return comparisons


def enrich_package(package: dict, snapshot: dict, previous_package: dict | None = None, *,
                   history_db: Path | None = None, previous_snapshot: Path | dict | None = None) -> dict:
    """Add source-matched windows, announced settlements and market confirmation."""
    generated_at = package.get("generated_at_bjt") or snapshot.get("generated_at_bjt")
    cutoff = _day(generated_at)
    if not cutoff:
        raise ValueError("A frozen generated_at_bjt is required")
    facts = package.setdefault("data", {}).setdefault("facts", {})
    investment = {"trend_facts": [], "calendar_facts": [], "market_facts": [], "coverage_facts": [], "comparison_facts": []}
    canonical = {str(r.get("id", "")).upper(): r for r in facts.get("canonical_metrics", []) if isinstance(r, dict)}
    series = {}
    for mid, row in canonical.items():
        if mid not in CORE_IDS:
            continue
        points, status = _metric_rows(row, snapshot, cutoff)
        if mid == "IORB":
            _effective_policy_rate(row, points, cutoff)
        series[mid] = points
        window_facts = _window_facts(mid, row.get("name", mid), points, row.get("unit"), row.get("frequency"),
                                     row.get("source"), [row.get("fact_id", f"metric:{mid}")])
        freshness, age = _freshness(row, cutoff)
        for item in window_facts:
            item.update(stale_days=age, source_status=row.get("status"), source_url=row.get("source_url"), status=freshness)
        investment["trend_facts"].extend(window_facts)
        available = [f["window_observations"] for f in window_facts]
        if len(available) < len(WINDOWS):
            investment["coverage_facts"].append(_coverage(
                f"history:{mid}", f"{mid}历史窗口不完整；只使用已提供窗口，不以单期变化外推。",
                as_of=row.get("as_of"), status=status if status != "ok" else "insufficient_history",
                base_ids=[row.get("fact_id", f"metric:{mid}")], observations=len(points), available_windows=available,
                frequency_label=_frequency_label(row.get("frequency")), missing_windows=[n for n in WINDOWS if n not in available]))
    # Explicitly match the policy anchor effective on each SOFR observation date.
    sofr, iorb = dict(series.get("SOFR", [])), dict(series.get("IORB", []))
    matched = sorted((d, (v - iorb[d]) * 100) for d, v in sofr.items() if d in iorb)
    sofr_row = canonical.get("SOFR", {})
    iorb_row = canonical.get("IORB", {})
    sofr_freshness, sofr_age = _freshness(sofr_row, cutoff)
    iorb_freshness, iorb_age = _freshness(iorb_row, cutoff)
    anchor_stale = sofr_freshness != "ok" or iorb_freshness != "ok"
    if matched:
        matched_age = (date.fromisoformat(cutoff) - date.fromisoformat(matched[-1][0])).days
        latest_matched = matched[-1][0] == _day(sofr_row.get("as_of"))
        matched_facts = _window_facts(
            "SOFR_IORB", "同日SOFR减IORB", matched, "bp", "daily matched observations",
            "NY Fed SOFR and canonical IORB; exact date join", ["metric:SOFR", "metric:IORB"], role="funding_price")
        for item in matched_facts:
            item.update(status="stale" if anchor_stale or not latest_matched else "ok", stale_days=matched_age,
                        matches_latest_sofr=latest_matched, matched_observations=len(matched),
                        sofr_source_status=sofr_row.get("status"), iorb_source_status=iorb_row.get("status"),
                        iorb_stale_days=iorb_age)
        investment["trend_facts"].extend(matched_facts)
    if anchor_stale:
        investment["coverage_facts"].append(_coverage(
            "sofr_iorb_freshness", "SOFR或IORB来源状态不完整或观测陈旧；同日匹配历史只作滞后背景，不能确认为当前融资压力。",
            as_of=sofr_row.get("as_of"), status="stale", base_ids=["metric:SOFR", "metric:IORB"],
            sofr_status=sofr_freshness, iorb_status=iorb_freshness, sofr_stale_days=sofr_age, iorb_stale_days=iorb_age))
    if len(matched) <= 60 or not matched or matched[-1][0] != _day(sofr_row.get("as_of")):
        investment["coverage_facts"].append(_coverage(
            "sofr_iorb_matching", "SOFR与IORB仅按共同观测日期匹配，不回填政策锚；未匹配或短窗口保持未知。",
            as_of=sofr_row.get("as_of"), status="incomplete_date_matched_history", base_ids=["metric:SOFR", "metric:IORB"],
            observations=len(matched), last_common_date=matched[-1][0] if matched else None))
    event_facts = facts.setdefault("event_facts", {})
    calendar_status = _settlement_sources(event_facts, snapshot, previous_package, history_db, generated_at)
    investment["calendar_facts"] = _calendar(event_facts, cutoff, calendar_status)
    embedded_context = package.get("data", {}).pop("market_context", None)
    context = snapshot.get("investment_market_context") or embedded_context or {}
    for sid, definition in MARKET_SERIES.items():
        info = context.get("series", {}).get(sid, {})
        rows = _points(context.get("price_history", {}).get(sid), cutoff)
        rows = [(d, v) for d, v in rows if v > 0]
        source_status = info.get("status", "missing")
        if rows:
            latest, previous = rows[-1], rows[-2] if len(rows) >= 2 else (None, None)
            age = (date.fromisoformat(cutoff) - date.fromisoformat(latest[0])).days
            status = "stale" if source_status == "ok" and age > (2 if sid == "CBBTCUSD" else 5) else source_status
            level_id = f"market:{sid}:level"
            investment["market_facts"].append({
                "fact_id": level_id, "id": sid, "name": definition["name"], "value": latest[1],
                "previous": previous[1], "change": latest[1] - previous[1] if previous[1] is not None else None,
                "unit": definition["unit"], "as_of": latest[0], "previous_as_of": previous[0],
                "frequency": definition["frequency"], "source": "FRED public CSV", "source_url": f"https://fred.stlouisfed.org/series/{sid}",
                "status": status, "source_status": source_status, "stale_days": age,
                "captured_at_bjt": info.get("captured_at_bjt"), "role": "market_confirmation",
                "base_fact_ids": [], "source_note": definition["source_note"],
            })
            windows = _window_facts(sid, definition["name"], rows, definition["unit"], definition["frequency"],
                                    "FRED public CSV", [level_id], prefix="market", role="market_confirmation", returns=True)
            for item in windows:
                item.update(status=status, source_status=source_status, stale_days=age,
                            source_url=f"https://fred.stlouisfed.org/series/{sid}")
            investment["market_facts"].extend(windows)
        if not rows or source_status != "ok" or age > (2 if sid == "CBBTCUSD" else 5):
            investment["coverage_facts"].append(_coverage(
                f"market:{sid}", f"{sid}市场确认数据缺失、离线缓存或滞后，不能当作当前价格确认。",
                as_of=rows[-1][0] if rows else None, status=status if rows else source_status, observations=len(rows),
                source_url=f"https://fred.stlouisfed.org/series/{sid}"))
    investment["comparison_facts"] = _package_comparisons(canonical, investment["market_facts"], previous_package or {}, previous_snapshot, generated_at)
    investment["coverage_facts"].extend([
        _coverage("direct_expectations", "未配置SOFR期货、调查共识或事件预期差；模型分解不能冒充市场直接预期，已计价程度保持未知。", as_of=cutoff),
        _coverage("btc_flows_leverage", "未配置BTC现货资金流及合约杠杆；美元流动性与价格确认不代表BTC全部收益驱动。", as_of=cutoff),
        _coverage("growth_earnings", "未配置增长与盈利修正；利率下降的股票影响需保留增长风险条件。", as_of=cutoff),
        _coverage("historical_vintages", "本次保存可见数据快照；回抓历史不等于当时可见版本，不能据此宣称无前视预测能力。", as_of=cutoff, status="prospective_capture_only"),
    ])
    facts["investment"] = investment
    package["investment_method_version"] = "3.1"
    return package

