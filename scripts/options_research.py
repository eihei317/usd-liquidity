"""Attach SPX option sensitivity and public futures-option positioning to a frozen run."""
from __future__ import annotations

from contextlib import closing
from itertools import groupby
import sqlite3

from .investment_facts import _metric_rows
from .investment_review import _timestamp
from .option_gamma_model import build_standard_gamma_history
from .option_volatility import build_volatility_spread_history

MODEL_ID = "option:SPX:model_delta_change_1pct"
POSITION_ID = "option:SP500_FUTURES:dealer_option_delta"
SPREAD_ID = "option:SPX:iv_minus_rv21"
OI_SHARE_ID = "option:SP500_FUTURES:option_oi_share"
REALIZED_ID = "option:SPX:realized_vol21"
CHAIN_SERIES = {
    "option:SPX:gross_gamma_1pct": ("SPX 期权持仓的无符号 Gamma 敞口", "USD per 1% SPX move"),
    "option:SPX:gamma_share_7d": ("七天内到期合约的 Gamma 占比", "%"),
    "option:SPX:gamma_share_0dte": ("当日到期合约的 Gamma 占比", "%"),
}
CFTC_URL = "https://www.cftc.gov/MarketReports/CommitmentsofTraders/ExplanatoryNotes/index.htm"


def _chain_signature(entry):
    # Freshness changes as the clock advances. Compare the underlying observation.
    return (entry.get("open_interest_as_of"), sorted((f["fact_id"], f["value"]) for f in entry.get("facts", [])),
            entry.get("strike_distribution", []), entry.get("coverage", {}).get("reason"))


def _conflicting_chain(entry):
    return {**entry, "status": "invalid", "facts": [], "strike_distribution": [],
            "source": None, "source_url": None, "coverage": {"reason": "conflicting_snapshot"}}


def capture_inputs(stamp, existing, chain_dir, *, fetch):
    """Replays read only the frozen capture. Local authorized inputs are aggregated before export."""
    from .option_chain import load_chain_history
    from .option_positioning import capture_positioning

    existing = existing or {}
    if not fetch:
        if existing.get("generated_at_bjt") == stamp:
            return existing
        return {"generated_at_bjt": stamp, "positioning": {}, "chains": []}

    imported = load_chain_history(chain_dir, stamp)
    # Keep prior authorized summaries after a source file is rotated. A later
    # vintage replaces only its matching observation when building the daily series.
    summaries = {}
    issues = [r for r in imported if not r.get("observed_at") or not r.get("available_at")]
    for item in [*existing.get("chains", []), *imported]:
        if item.get("observed_at") and item.get("available_at") and _timestamp(item["available_at"]) <= _timestamp(stamp):
            key = (item["observed_at"], item["available_at"], item.get("source"), item.get("source_url"))
            if key in summaries and _chain_signature(summaries[key]) != _chain_signature(item):
                item = {**_conflicting_chain(item), "source": item.get("source"), "source_url": item.get("source_url")}
            summaries[key] = item
    return {"generated_at_bjt": stamp, "positioning": capture_positioning(stamp),
            "chains": list(summaries.values()), "chain_issues": issues}


def _latest_fact(history, fid, name, unit, source, url, frequency, parents):
    points = history.get("points") or []
    end = points[-1] if points else {}
    prior = points[-2] if len(points) > 1 else {}
    value, previous = end.get("value"), prior.get("value")
    return {
        "fact_id": fid, "id": fid.rsplit(":", 1)[-1], "name": name, "unit": unit, "value": value,
        "as_of": end.get("date"), "previous": previous, "previous_as_of": prior.get("date"),
        "change": value - previous if value is not None and previous is not None else None,
        "status": history.get("status", "missing"), "source_status": history.get("source_status", "missing"),
        "source": source, "source_url": url, "frequency": frequency,
        "role": "equity_derivatives", "base_fact_ids": parents, "observations": len(points),
        "message": history.get("message") or ("该次快照缺少可用的同期观测。" if value is None else ""),
    }


def _chain_history(capture, stamp):
    cutoff = _timestamp(stamp)
    entries = [item for item in capture.get("chains", []) if _timestamp(item["available_at"]) <= cutoff
               and _timestamp(item["observed_at"]) <= cutoff]
    def vintage(item):
        return _timestamp(item["observed_at"]), _timestamp(item["available_at"])
    entries.sort(key=vintage)
    resolved = []
    for _, reports in groupby(entries, key=vintage):
        batch = list(reports)
        entry = batch[0]
        if any(_chain_signature(item) != _chain_signature(entry) for item in batch[1:]):
            entry = _conflicting_chain(entry)
        resolved.append(entry)
    entries = resolved
    days = {sid: {} for sid in CHAIN_SERIES}
    for entry in entries:
        # Last available snapshot of each observation day is the historical daily point.
        observed_day = entry["as_of"]
        for sid in days:
            days[sid].pop(observed_day, None)
        for fact in entry.get("facts", []):
            if fact.get("fact_id") in days and fact.get("value") is not None:
                days[fact["fact_id"]][observed_day] = fact["value"]
    series = {sid: [{"date": d, "value": v} for d, v in sorted(values.items())] for sid, values in days.items()}

    issues = capture.get("chain_issues") or []
    if entries:
        chain = dict(entries[-1])
        age = cutoff - _timestamp(chain["observed_at"])
        from .option_chain import MAX_QUOTE_AGE
        if age > MAX_QUOTE_AGE and chain.get("status") == "ok":
            chain["status"] = "stale"
        chain["stale_days"] = age.days
        chain["facts"] = [{**f, "name": CHAIN_SERIES[f["fact_id"]][0], "status": chain["status"],
                           "source_url": chain.get("source_url"), "role": "equity_derivatives"} for f in chain["facts"]]
    else:
        chain = {"status": "not_configured", "scope": "SPX+SPXW", "as_of": None, "facts": [],
                 "coverage": {}, "message": "本次快照没有可用于本项目的 SPX/SPXW 逐合约持仓数据。"}
    if issues:
        chain["input_status"] = [i.get("status", "invalid") for i in issues]
        if not entries:
            chain.update(status=issues[-1].get("status", "invalid"), message=issues[-1].get("message") or "本次期权链未通过覆盖或授权检查。")
    return chain, series


def _coverage(fid, name, points, source, *, optional=False):
    return {"kind": "options", "id": fid, "name": name, "source": source, "observations": len(points),
            "first": points[0]["date"] if points else None, "last": points[-1]["date"] if points else None,
            "status": "history_available" if len(points) > 1 else "missing_history", "optional": optional}


def _prior_reference(points, window, *, weekly=False):
    """Percent of strictly earlier comparable observations at or below today's value."""
    recent = points[-(window + 1):]
    if weekly:
        # The first point after a missing week or contract change starts a fresh comparison window.
        last_break = max((i for i, row in enumerate(recent) if row["change"] is None), default=0)
        recent = recent[last_break:]
    prior = recent[:-1]
    count = len(prior)
    below = sum(row["value"] <= recent[-1]["value"] for row in prior)
    return {"window": window, "count": count, "at_or_below": below if count else None,
            "percentile": 100 * below / count if count == window else None,
            "high": max(row["value"] for row in prior) if count == window else None,
            "start": prior[0]["date"] if count else None, "end": prior[-1]["date"] if count else None}


def _persist(db, series, source_histories, oi_histories):
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS option_indicator_history
                        (series_id TEXT NOT NULL, as_of TEXT NOT NULL, value REAL NOT NULL,
                         unit TEXT NOT NULL, contract_multiplier REAL, PRIMARY KEY (series_id, as_of))""")
        for fid, (_, unit, _, points) in series.items():
            conn.execute("DELETE FROM option_indicator_history WHERE series_id=?", (fid,))
            conn.executemany("INSERT INTO option_indicator_history VALUES (?,?,?,?,?)",
                             ((fid, row["date"], row["value"], unit, row.get("contract_multiplier")) for row in points))
        conn.execute("""CREATE TABLE IF NOT EXISTS option_cftc_source_history
                        (report TEXT NOT NULL, as_of TEXT NOT NULL, dealer_long INTEGER NOT NULL, dealer_short INTEGER NOT NULL,
                         contract_multiplier REAL NOT NULL, PRIMARY KEY (report, as_of))""")
        for report, points in source_histories.items():
            conn.execute("DELETE FROM option_cftc_source_history WHERE report=?", (report,))
            conn.executemany("INSERT INTO option_cftc_source_history VALUES (?,?,?,?,?)",
                             ((report, p["date"], p["dealer_long"], p["dealer_short"], p["contract_multiplier"]) for p in points))
        conn.execute("""CREATE TABLE IF NOT EXISTS option_cftc_open_interest_history
                        (report TEXT NOT NULL, as_of TEXT NOT NULL, open_interest INTEGER NOT NULL,
                         contract_multiplier REAL NOT NULL, PRIMARY KEY (report, as_of))""")
        for report, points in oi_histories.items():
            conn.execute("DELETE FROM option_cftc_open_interest_history WHERE report=?", (report,))
            conn.executemany("INSERT INTO option_cftc_open_interest_history VALUES (?,?,?,?)",
                             ((report, p["date"], p["open_interest"], p["contract_multiplier"]) for p in points))


def _source_coverage(histories):
    return {name: {"observations": len(rows), "first": rows[0]["date"] if rows else None,
                   "last": rows[-1]["date"] if rows else None} for name, rows in histories.items()}


def _chart_gaps(coverage, *fields):
    dates = set().union(*(coverage.get(key, []) for key in fields))
    for source in coverage.get("source_gaps", {}).values():
        dates.update(source["invalid_or_conflicting_dates"])
    return dates


def attach_options(package, snapshot, market, capture, db):
    from .option_positioning import build_positioning_history

    stamp = package["generated_at_bjt"]
    data = package["data"]["facts"]
    canonical = next((r for r in data["canonical_metrics"] if r["id"] == "VIXCLS"), {})
    vix_points, vix_status = _metric_rows(canonical, snapshot, stamp[:10])
    prices = market.get("price_history", {})
    markets = market.get("series", {})
    spot = prices.get("SP500", [])
    source_statuses = {"sp500_status": markets.get("SP500", {}).get("status", "missing"),
                       "vix_status": canonical.get("status", "missing") if vix_status == "ok" else vix_status}
    sessions = prices.get("NASDAQCOM") if markets.get("NASDAQCOM", {}).get("status") in ("ok", "stale") else None
    model = build_standard_gamma_history(spot, vix_points, stamp, **source_statuses)
    spread = build_volatility_spread_history(spot, vix_points, stamp, **source_statuses, equity_session_rows=sessions)
    position = build_positioning_history(capture.get("positioning") or {}, stamp)
    model_fact = _latest_fact(model, MODEL_ID, model["name"], "Delta百分点/标的变动1%", "FRED SP500、VIXCLS；欧式平值模型",
                              "https://fred.stlouisfed.org/series/VIXCLS", "daily", ["market:SP500:level", "metric:VIXCLS"])
    model_fact.update(method=model["metadata"]["method"], limitations=model["metadata"]["limitations"], interpretation=model["metadata"]["interpretation"],
                      source_statuses=model["source_statuses"],
                      measurement="model_gamma", stale_days=model.get("stale_days"))
    if model["points"]:
        model_fact["gamma_per_index_point"] = model["points"][-1]["gamma_per_point"]
    spread_fact = _latest_fact(spread, SPREAD_ID, spread["name"], "波动率点", "FRED SP500、VIXCLS",
                               model_fact["source_url"], "daily", model_fact["base_fact_ids"])
    spread_fact.update(measurement=spread["metadata"]["method_version"], source_statuses=spread["source_statuses"],
                       method=spread["metadata"]["method"], limitations=spread["metadata"]["limitations"],
                       stale_days=spread["stale_days"], reference=_prior_reference(spread["points"], 252))
    if spread["points"]:
        end = spread["points"][-1]
        spread_fact.update(vix_pct=end["vix_pct"], realized_vol_pct=end["realized_vol_pct"],
                           realized_window_start=end["window_start"], return_count=end["return_count"])
    pos_fact = _latest_fact(position, POSITION_ID, "标普500期货期权交易商净方向敞口估计", "等值期货手",
                            "CFTC Traders in Financial Futures · 13874+", CFTC_URL, "weekly", [])
    pos_fact.update(measurement="futures_equivalent_delta", source_statuses=position.get("source_statuses", {}),
                    source_captured_at_bjt=position.get("source_captured_at_bjt"), stale_days=position.get("stale_days"),
                    interpretation=position["interpretation"], limitations=position["limitations"],
                    method="同周合并报表的交易商多头减空头，再减去仅期货报表的交易商多头减空头。")
    share = position["open_interest_share"]
    share_fact = _latest_fact(share, OI_SHARE_ID, "CME 标普期货市场的期权持仓占比", "%", pos_fact["source"], CFTC_URL, "weekly", [])
    share_fact.update(measurement="delta_equivalent_oi_share_v1", source_captured_at_bjt=share["source_captured_at_bjt"],
                      source_statuses=share["source_statuses"], stale_days=share["stale_days"],
                      method="合并报表总未平仓量减去仅期货报表总未平仓量，再除以合并报表总未平仓量，按百分数展示。",
                      interpretation=share["interpretation"], limitations=share["limitations"],
                      reference=_prior_reference(share["points"], 52, weekly=True))
    for fact, history, legs in ((pos_fact, position, ("combined_net", "futures_only_net")),
                                (share_fact, share, ("combined_oi", "futures_only_oi"))):
        if history["points"]:
            last = history["points"][-1]
            fact.update({k: last[k] for k in (*legs, "contract_multiplier", "change")})
            if last["change"] is None:
                fact.update(previous=None, previous_as_of=None)
    chain, chain_series = _chain_history(capture, stamp)
    limit = {"fact_id": "coverage:spx_dealer_gamma", "status": "missing", "as_of": stamp[:10],
             "message": "缺少按参与者分拆的做市商净 Gamma 与实际对冲成交。当前输入无法确认做市商对冲方向或 Gamma 挤压。"}
    options = {"model": model_fact, "positioning": pos_fact, "volatility_spread": spread_fact,
               "open_interest_share": share_fact, "chain": chain, "coverage_facts": [limit]}
    data["investment"]["options"] = options
    series = {fact["fact_id"]: (fact["name"], fact["unit"], fact["source"], history["points"])
              for fact, history in ((spread_fact, spread), (share_fact, share), (model_fact, model), (pos_fact, position))}
    series[REALIZED_ID] = ("标普500近21个交易日的年化实际波动率", "%", "FRED SP500", spread["realized_points"])
    for sid, points in chain_series.items():
        series[sid] = (*CHAIN_SERIES[sid], "授权 SPX/SPXW 逐合约期权链汇总", points)
    _persist(db, series, position["source_histories"], position["source_open_interest_histories"])
    weekly_gaps = ("missing_combined_dates", "missing_futures_only_dates", "missing_both_week_starts", "incompatible_unit_dates")
    gaps = {SPREAD_ID: _chart_gaps(spread["coverage"], "interrupted_window_dates", "insufficient_window_dates", "missing_vix_dates"),
            POSITION_ID: _chart_gaps(position["coverage"], *weekly_gaps),
            OI_SHARE_ID: _chart_gaps(share["coverage"], *weekly_gaps, "zero_combined_oi_dates", "futures_oi_exceeds_combined_dates")}
    audit, charts = [], []
    for fid, (name, unit, source, points) in series.items():
        row = _coverage(fid, name, points, source, optional=fid in CHAIN_SERIES)
        audit.append(row)
        if points and fid != REALIZED_ID:
            weekly = fid in (POSITION_ID, OI_SHARE_ID)
            shown = points[-(104 if weekly else 252):]
            if weekly:
                # Older CFTC reports used a different multiplier. Do not connect different contract sizes.
                cut = max((i + 1 for i, p in enumerate(shown) if p["contract_multiplier"] != shown[-1]["contract_multiplier"]), default=0)
                shown = shown[cut:]
            chart_points = [{"date": point["date"], "value": point["value"], **({"change": point["change"]} if weekly else {})} for point in shown]
            if fid in gaps:
                chart_points.extend({"date": day, "value": None} for day in gaps[fid] if shown[0]["date"] < day < shown[-1]["date"])
                chart_points.sort(key=lambda point: point["date"])
            charts.append({"id": "options_" + fid.rsplit(":", 1)[-1], "title": name, "chart_type": "line", "unit": unit,
                           "series": [{"id": fid, "label": name, "points": chart_points, "y_axis": "y"}]})
    observed_chain_days = {r["as_of"] for r in capture.get("chains", []) if r.get("as_of") and r["as_of"] <= stamp[:10]}
    trading_days = {p["date"] for p in market.get("price_history", {}).get("SP500", []) if isinstance(p, dict) and p.get("date")}
    first_chain_day = min(observed_chain_days, default=None)
    missing_snapshots = sorted(d for d in trading_days - observed_chain_days if first_chain_day and first_chain_day <= d <= stamp[:10])
    details = {"model": model["coverage"], "positioning": {**position["coverage"], "source_histories": _source_coverage(position["source_histories"])},
               "volatility_spread": spread["coverage"],
               "open_interest_share": {**share["coverage"], "source_histories": _source_coverage(position["source_open_interest_histories"])},
               "chain": {"status": chain["status"], "coverage": chain.get("coverage", {}), "input_status": chain.get("input_status", []),
                         "missing_snapshot_dates": missing_snapshots,
                         "missing_fact_dates": {fid: sorted(observed_chain_days - {p["date"] for p in points}) for fid, points in chain_series.items()},
                         "available_snapshots": len(capture.get("chains", []))}}
    return audit, details, charts
