"""Summarize a licensed local standard SPX/SPXW chain. No network access or writes.

The local JSON contract is documented in docs/options_gamma.md. Only the numbers
and metadata constructed here can leave this module. Never return input rows,
filenames, download URLs, license text or an input-related exception message.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DESTINATION = "github.com/eihei317/usd-liquidity"
SCOPE = "all_unexpired_standard_SPX_SPXW"
MAX_QUOTE_AGE = timedelta(days=4)
MAX_OI_AGE_DAYS = 7
try:
    NEW_YORK = ZoneInfo("America/New_York")
except ZoneInfoNotFoundError:
    NEW_YORK = None


def _instant(value):
    if isinstance(value, datetime):
        stamp = value
    elif isinstance(value, str):
        try:
            stamp = datetime.fromisoformat(value.strip().replace(" UTC", "").replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        return None
    return stamp.astimezone(timezone.utc)


def _ny_day(stamp):
    if NEW_YORK is not None:
        return stamp.astimezone(NEW_YORK).date()
    # Windows embedded Python ships without IANA tzdata. US rules since 2007
    # switch at 07:00 UTC on the second March Sunday and 06:00 on the first
    # November Sunday. Refuse earlier inputs when tzdata is unavailable.
    if stamp.year < 2007:
        raise ValueError("unsupported historic New York timezone")
    march, november = date(stamp.year, 3, 8), date(stamp.year, 11, 1)
    start = datetime.combine(march + timedelta(days=(6 - march.weekday()) % 7), datetime.min.time(), timezone.utc).replace(hour=7)
    end = datetime.combine(november + timedelta(days=(6 - november.weekday()) % 7), datetime.min.time(), timezone.utc).replace(hour=6)
    return (stamp - timedelta(hours=4 if start <= stamp < end else 5)).date()


def _day(value):
    if not isinstance(value, str) or len(value) != 10:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _empty(status, reason):
    return {"status": status, "scope": "SPX+SPXW", "as_of": None, "observed_at": None, "available_at": None,
            "open_interest_as_of": None, "source": None, "source_url": None, "facts": [], "strike_distribution": [],
            "coverage": {"reason": reason}}


def _source(payload):
    name, link = payload.get("source"), payload.get("source_url")
    if not isinstance(name, str) or not 1 <= len(name.strip()) <= 80 or any(c in name for c in "\r\n@:/=?"):
        return None
    if not isinstance(link, str):
        return None
    parsed = urlsplit(link)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        return None
    # Only the public vendor origin is exported. Even a path can contain a credential.
    return name.strip(), f"https://{parsed.hostname}"


def _chain_rows(payload, observed, day):
    rows = {}
    counts = {"listed_rows": len(payload["contracts"]), "eligible_contracts": 0, "expired_contracts": 0,
              "duplicate_rows": 0, "missing_contracts": 0, "same_day_timing_missing": 0}
    for row in payload["contracts"]:
        if not isinstance(row, dict):
            return None, counts, "invalid_contract"
        root, right, strike = row.get("root"), row.get("right"), row.get("strike")
        expiry = _day(row.get("expiration"))
        if root not in ("SPX", "SPXW") or right not in ("C", "P") or not _number(strike) or strike <= 0 or not expiry:
            return None, counts, "invalid_contract_identity"
        if row.get("contract_multiplier", 100) != 100 or row.get("gamma_unit", "delta_per_index_point") != "delta_per_index_point":
            return None, counts, "inconsistent_contract_units"
        expires = _instant(row.get("expires_at"))
        last_trade = _instant(row.get("last_trade_at"))
        if (row.get("expires_at") is not None and (not expires or _ny_day(expires) != expiry)
                or row.get("last_trade_at") is not None and (not last_trade or _ny_day(last_trade) > expiry)
                or expires and last_trade and last_trade > expires):
            return None, counts, "invalid_expiration_timing"
        key = root, expiry, strike, right
        gamma, oi = row.get("gamma"), row.get("open_interest")
        if gamma is not None and (not _number(gamma) or gamma < 0):
            return None, counts, "invalid_gamma"
        if oi is not None and (type(oi) is not int or oi < 0):
            return None, counts, "invalid_open_interest"
        item = gamma, oi, expires, last_trade
        if key in rows:
            if rows[key] != item:
                return None, counts, "conflicting_duplicate"
            counts["duplicate_rows"] += 1
        else:
            rows[key] = item
    grouped = defaultdict(list)
    short_dated, tradable_today = [], []
    factor = 100 * payload["spot"] ** 2 * 0.01
    for (_, expiry, strike, _), (gamma, oi, expires, last_trade) in rows.items():
        if expiry < day or expires and expires <= observed:
            counts["expired_contracts"] += 1
            continue
        counts["eligible_contracts"] += 1
        if gamma is None or oi is None:
            counts["missing_contracts"] += 1
            continue
        amount = gamma * oi * factor
        if not math.isfinite(amount):
            return None, counts, "invalid_gamma_amount"
        grouped[strike].append(amount)
        if (expiry - day).days <= 7:
            short_dated.append(amount)
        if expiry == day:
            if expires is None or last_trade is None:
                counts["same_day_timing_missing"] += 1
            elif observed < last_trade:
                tradable_today.append(amount)
    return ({strike: math.fsum(amounts) for strike, amounts in grouped.items()},
            math.fsum(short_dated), math.fsum(tradable_today)), counts, None


def _summarize(payload, generated_at_bjt):
    if not isinstance(payload, dict):
        return _empty("invalid", "invalid_snapshot")
    available, cutoff = _instant(payload.get("available_at")), _instant(generated_at_bjt)
    if available and cutoff and available > cutoff:
        return _empty("unavailable_at_cutoff", "capture_not_yet_available")
    if payload.get("allowed_aggregate_destination") != DESTINATION:
        return _empty("redistribution_unconfirmed", "aggregate_destination_not_authorized")
    stamp = _instant(payload.get("observed_at"))
    if not stamp or not available or not cutoff or available < stamp:
        return _empty("invalid", "invalid_capture_timing")
    day = _ny_day(stamp)
    oi_day = _day(payload.get("open_interest_as_of"))
    source = _source(payload)
    if (type(payload.get("schema_version")) is not int or payload["schema_version"] != 1
            or payload.get("underlying") != "SPX" or payload.get("scope") != SCOPE
            or payload.get("contract_multiplier") != 100 or payload.get("gamma_unit") != "delta_per_index_point"
            or not _number(payload.get("spot")) or payload["spot"] <= 0 or not oi_day or oi_day > day or not source):
        return _empty("invalid", "invalid_snapshot_metadata")
    result = _empty("partial", "incomplete_chain")
    result.update(as_of=day.isoformat(), observed_at=stamp.isoformat(), available_at=available.isoformat(),
                  open_interest_as_of=oi_day.isoformat(), source=source[0], source_url=source[1])
    contracts = payload.get("contracts")
    session_open = payload.get("session_open_at_observation")
    if (type(payload.get("complete_chain")) is not bool or not isinstance(contracts, list)
            or session_open is not None and type(session_open) is not bool):
        result.update(status="invalid", coverage={"reason": "invalid_chain_declaration"})
        return result
    if not contracts:
        result.update(status="missing", coverage={"reason": "empty_chain"})
        return result
    values, counts, error = _chain_rows(payload, stamp, day)
    result["coverage"] = counts
    if error:
        result.update(status="invalid")
        counts["reason"] = error
        return result
    if not payload["complete_chain"] or counts["missing_contracts"] or not counts["eligible_contracts"]:
        counts["reason"] = "incomplete_chain" if not payload["complete_chain"] else "missing_gamma_or_oi" if counts["missing_contracts"] else "no_active_contracts"
        return result
    quote_stale = cutoff - stamp > MAX_QUOTE_AGE
    oi_stale = (day - oi_day).days > MAX_OI_AGE_DAYS
    status = "stale" if quote_stale or oi_stale else "ok"
    result["status"] = status
    counts.update(reason="complete", quote_stale=quote_stale, oi_stale=oi_stale,
                  session_open_at_observation=session_open)
    buckets, near, today = values
    total = math.fsum(buckets.values())
    base = {"as_of": result["as_of"], "source": source[0], "status": status}
    def fact(fid, value, unit):
        return {**base, "fact_id": "option:SPX:" + fid, "value": value, "unit": unit}
    result["facts"] = [fact("gross_gamma_1pct", total, "USD per 1% SPX move")]
    if total > 0:
        result["facts"].append(fact("gamma_share_7d", 100 * (near / total), "%"))
        if session_open is True and not counts["same_day_timing_missing"]:
            result["facts"].append(fact("gamma_share_0dte", 100 * (today / total), "%"))
        result["strike_distribution"] = [
            {"strike": strike, "gross_gamma_usd_1pct": value, "share_pct": 100 * (value / total)}
            for strike, value in sorted(buckets.items(), key=lambda item: (-item[1], item[0]))[:5] if value > 0
        ]
    return result


def summarize_chain(payload, generated_at_bjt):
    """Return only the authorized aggregate visible by the supplied aware cutoff."""
    try:
        return _summarize(payload, generated_at_bjt)
    except (ValueError, OverflowError):
        return _empty("invalid", "unrepresentable_input")


def summarize_chain_file(path, generated_at_bjt):
    def unique_fields(pairs):
        record = dict(pairs)
        if len(record) != len(pairs):
            raise ValueError("duplicate JSON field")
        return record
    try:
        with Path(path).open(encoding="utf-8-sig") as stream:
            return summarize_chain(json.load(stream, object_pairs_hook=unique_fields), generated_at_bjt)
    except FileNotFoundError:
        return _empty("missing", "file_not_found")
    except (OSError, UnicodeError, ValueError, RecursionError):
        return _empty("invalid", "unreadable_snapshot")


def load_chain_history(directory, generated_at_bjt):
    """Read local *.json captures. Different release times preserve revisions."""
    if not directory or not Path(directory).is_dir():
        return []
    snapshots, undated = {}, []
    for path in sorted(Path(directory).glob("*.json")):
        row = summarize_chain_file(path, generated_at_bjt)
        if row["status"] == "unavailable_at_cutoff":
            continue
        if not row["available_at"]:
            if row not in undated:
                undated.append(row)
            continue
        key = row["available_at"], row["observed_at"], row["source"], row["source_url"]
        if key in snapshots and snapshots[key] != row:
            row.update(status="invalid", facts=[], strike_distribution=[], coverage={"reason": "conflicting_snapshot"})
        snapshots[key] = row
    return undated + [snapshots[key] for key in sorted(snapshots)]
