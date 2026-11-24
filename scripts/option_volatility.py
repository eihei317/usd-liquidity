"""Pair the closing VIX with trailing realized volatility from the frozen equity closes."""
from __future__ import annotations

import math
from collections import deque
from datetime import date
from statistics import stdev

from .option_gamma_model import _day, _observations


RETURN_COUNT = 21
ANNUALIZATION = 252
# Nasdaq's frozen history reports a value on this confirmed cash-market holiday.
# Record the evidence instead of making the daily schedule depend on one stray quote.
_CONFIRMED_REFERENCE_CLOSURES = {
    "2019-04-19": {
        "reason": "NYSE 确认当日为 Good Friday，现金股票市场休市。NASDAQCOM 的孤立读数不能证明存在标普收盘。",
        "source_url": "https://ir.theice.com/press/news-details/2018/NYSE-Group-Announces-2019-2020-and-2021-Holiday-and-Early-Closings-Calendar/default.aspx",
    },
}


def build_volatility_spread_history(sp500_rows, vix_rows, cutoff, *, sp500_status="ok", vix_status="ok",
                                    equity_session_rows=None):
    """Estimate RV from 22 consecutive observed SPX closes, matching VIX only at the endpoint.

    Optional Nasdaq Composite closes provide positive evidence that US cash equities traded.
    A VIX-only date inside that reference's span is recorded separately because index options
    can quote on cash-market holidays. A date outside its span is unresolved. No return is
    formed across a confirmed bad/missing SPX close or an unresolved VIX-only date.
    """
    cutoff = _day(cutoff)
    if cutoff is None:
        raise ValueError("cutoff must contain an ISO observation date")
    spot, spot_gaps = _observations(sp500_rows, cutoff)
    vix, vix_gaps = _observations(vix_rows, cutoff)
    sessions, session_gaps = _observations(equity_session_rows, cutoff)
    bad_spot = set(spot_gaps["invalid_dates"] + spot_gaps["conflicting_dates"])
    spot_dates = spot.keys() | bad_spot
    first_spot = min(spot_dates, default=cutoff)
    first_session, last_session = min(sessions, default=None), max(sessions, default=None)
    bad_session_dates = set(session_gaps["invalid_dates"] + session_gaps["conflicting_dates"])

    conflicting_closures = {day for day in (sessions.keys() | vix.keys()) - spot_dates
                            if day >= first_spot and day in _CONFIRMED_REFERENCE_CLOSURES}
    missing_cash = {day for day in sessions.keys() - spot_dates - conflicting_closures if day >= first_spot}
    vix_only = {day for day in vix.keys() - spot_dates - sessions.keys() if day >= first_spot}
    unconfirmed_sessions = {day for day in vix_only - conflicting_closures
                            if first_session is None or not first_session <= day <= last_session or day in bad_session_dates}
    breaks = bad_spot | missing_cash | unconfirmed_sessions
    prices = deque(maxlen=RETURN_COUNT + 1)
    points, realized_points, warmup = [], [], []
    for day in sorted(spot.keys() | breaks):
        if day in breaks:
            prices.clear()
            continue
        prices.append((day, math.log(spot[day][0])))
        if len(prices) < RETURN_COUNT + 1:
            warmup.append(day)
            continue
        log_prices = [price for _, price in prices]
        returns = [today - previous for previous, today in zip(log_prices, log_prices[1:])]
        realized = stdev(returns) * math.sqrt(ANNUALIZATION) * 100
        realized_points.append({"date": day, "value": realized})
        if day not in vix:
            continue
        implied, vix_capture = vix[day]
        point = {"date": day, "value": implied - realized, "vix_pct": implied, "realized_vol_pct": realized,
                 "window_start": prices[0][0], "window_end": day, "return_count": RETURN_COUNT}
        if spot[day][1]:
            point["sp500_captured_at_bjt"] = spot[day][1]
        if vix_capture:
            point["vix_captured_at_bjt"] = vix_capture
        points.append(point)

    statuses = {"SP500": sp500_status or "unknown", "VIXCLS": vix_status or "unknown"}
    source_status = next((status for status in statuses.values() if status != "ok"), "ok")
    latest = points[-1]["date"] if points else None
    age = (date.fromisoformat(cutoff) - date.fromisoformat(latest)).days if latest else None
    status = source_status
    if source_status == "ok":
        if not latest:
            status = "missing"
        elif age > 5:
            status = "stale"
        elif latest < max(spot.keys() | breaks):
            status = "partial_latest"
    return {
        "series_id": "SPX_VIX_MINUS_RV21", "name": "标普500隐含波动率减近期实际波动率",
        "as_of": latest, "status": status, "source_status": source_status, "source_statuses": statuses,
        "stale_days": age, "points": points, "realized_points": realized_points,
        "metadata": {
            "method_version": "vix_minus_trailing_rv21_v1", "return_count": RETURN_COUNT,
            "annualization": ANNUALIZATION, "unit": "年化波动率百分点",
            "method": "用标普500连续22个收盘价计算21个日对数收益，取样本标准差乘以√252并换算为百分数。用同日收盘VIX减去该值。",
            "interpretation": "正值表示期权报出的未来30个自然日波动高于过去21个交易日收盘涨跌的实际波动。",
            "limitations": "仅用日收盘估计近期振幅。这个价差不能直接估算未来实现波动、期权盈亏或股市方向。",
            "session_evidence": "用纳指综合收盘日期核对现金市场是否开市，遇到冲突时采用交易所确认的休市日。仅有VIX的日期单独列示。所有来源共同缺报的交易日无法从这些数据识别。",
        },
        "coverage": {
            "cutoff": cutoff, "observations": len(points), "first_common_as_of": points[0]["date"] if points else None,
            "latest_common_as_of": latest, "latest_sp500_as_of": max(spot, default=None), "latest_vix_as_of": max(vix, default=None),
            "sp500_gaps": spot_gaps, "vix_gaps": vix_gaps,
            "session_reference_first": first_session, "session_reference_last": last_session,
            "confirmed_reference_closures": {d: _CONFIRMED_REFERENCE_CLOSURES[d] for d in sorted(conflicting_closures)},
            "missing_sp500_session_dates": sorted(missing_cash), "missing_vix_dates": sorted(spot.keys() - vix.keys()),
            "vix_only_dates_within_reference": sorted(vix_only - unconfirmed_sessions - conflicting_closures),
            "unconfirmed_session_dates": sorted(unconfirmed_sessions), "interrupted_window_dates": sorted(breaks),
            "insufficient_window_dates": warmup,
        },
    }
