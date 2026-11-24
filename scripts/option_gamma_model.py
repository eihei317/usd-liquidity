"""Offline 30-calendar-day ATM SPX option model using coincident SP500 and VIX closes."""
from __future__ import annotations

import math
from datetime import date


SERIES_ID = "SPX_ATM30D_GAMMA_PROXY"
_T = 30 / 365
_SQRT_T = math.sqrt(_T)
_SQRT_2PI = math.sqrt(2 * math.pi)
_SOURCES = {
    "SP500": "https://fred.stlouisfed.org/series/SP500",
    "VIXCLS": "https://fred.stlouisfed.org/series/VIXCLS",
}


def _positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def standard_gamma(spot, vix_pct):
    """Return unit delta gamma and its local change in points per +1% spot move.

    Each date starts a new model European call/put at K=S. When differentiating
    the option, hold that strike, volatility, maturity and rates fixed.
    """
    if not _positive(spot) or not _positive(vix_pct):
        raise ValueError("SP500 and VIXCLS must be positive finite observations")
    vol_time = vix_pct / 100 * _SQRT_T
    if vol_time == 0:
        raise ValueError("VIXCLS is too small to evaluate the model")
    d1 = vol_time / 2
    # 100 percentage points per unit delta × 1% spot move × gamma = S × gamma.
    delta_pp = math.exp(-0.5 * d1 * d1) / _SQRT_2PI / vol_time
    gamma = delta_pp / spot
    if not math.isfinite(gamma) or not math.isfinite(delta_pp) or gamma <= 0:
        raise ValueError("The input is outside the representable gamma range")
    return {"value": delta_pp, "gamma_per_point": gamma}


def _day(value):
    if not isinstance(value, (str, date)):
        return None
    text = str(value)
    if len(text) > 10 and text[10] not in (" ", "T"):
        return None
    try:
        return date.fromisoformat(text[:10]).isoformat()
    except ValueError:
        return None


def _observations(rows, cutoff):
    by_day, conflicts, invalid, future = {}, set(), set(), set()
    undated = 0
    for row in rows or ():
        captured = None
        if isinstance(row, dict):
            day, value = _day(row.get("date") or row.get("as_of")), row.get("value")
            captured = row.get("captured_at_bjt")
        elif isinstance(row, (list, tuple)) and len(row) == 2:
            day, value = _day(row[0]), row[1]
        else:
            day, value = None, None
        if not day:
            undated += 1
        elif day > cutoff:
            future.add(day)
        elif not _positive(value):
            invalid.add(day)
        elif day in by_day and by_day[day][0] != value:
            conflicts.add(day)
        else:
            # Preserve the latest known capture of an identical observation.
            prior_capture = by_day.get(day, (None, None))[1]
            stamp = max((s for s in (prior_capture, captured) if isinstance(s, str)), default=None)
            by_day[day] = (value, stamp)
    for day in conflicts | invalid:
        by_day.pop(day, None)
    return by_day, {
        "invalid_dates": sorted(invalid), "conflicting_dates": sorted(conflicts),
        "after_cutoff_dates": sorted(future), "undated_rows": undated,
    }


def build_standard_gamma_history(sp500_rows, vix_rows, cutoff, *, sp500_status="ok", vix_status="ok"):
    """Rebuild all valid common dates from a single frozen pair of source histories.

    Amounts, open interest and dealer positions are outside this model. Source
    failures and unmatched dates remain visible. No calendar or source is filled.
    """
    cutoff = _day(cutoff)
    if cutoff is None:
        raise ValueError("cutoff must contain an ISO observation date")
    spot, spot_gaps = _observations(sp500_rows, cutoff)
    vol, vol_gaps = _observations(vix_rows, cutoff)
    points, model_errors = [], []
    for day in sorted(spot.keys() & vol.keys()):
        price, price_capture = spot[day]
        vix, vix_capture = vol[day]
        try:
            point = standard_gamma(price, vix)
        except ValueError:
            model_errors.append(day)
            continue
        point.update(date=day, spot=price, vix_pct=vix)
        if price_capture:
            point["sp500_captured_at_bjt"] = price_capture
        if vix_capture:
            point["vix_captured_at_bjt"] = vix_capture
        points.append(point)
    statuses = {"SP500": sp500_status or "unknown", "VIXCLS": vix_status or "unknown"}
    source_status = next((s for s in statuses.values() if s != "ok"), "ok")
    latest = points[-1]["date"] if points else None
    observed_dates = (spot.keys() | vol.keys() | set(spot_gaps["invalid_dates"] + spot_gaps["conflicting_dates"])
                      | set(vol_gaps["invalid_dates"] + vol_gaps["conflicting_dates"]))
    age = (date.fromisoformat(cutoff) - date.fromisoformat(latest)).days if latest else None
    status = source_status
    if source_status == "ok":
        if not latest:
            status = "missing"
        elif age > 5:
            status = "stale"
        elif latest < max(observed_dates):
            status = "partial_latest"
    return {
        "series_id": SERIES_ID, "name": "标普500标准平值期权的30天模型Gamma",
        "as_of": latest, "status": status, "source_status": source_status, "source_statuses": statuses,
        "stale_days": age, "points": points,
        "metadata": {
            "method_version": "european_atm_30d_vix_v1",
            "unit": "delta percentage points per 1% spot move", "gamma_unit": "delta per index point",
            "days_to_expiry": 30, "day_count": "ACT/365 fixed", "strike": "K=S",
            "exercise": "European", "annual_rate": 0, "annual_dividend_yield": 0,
            "volatility": "VIXCLS / 100", "sources": _SOURCES.copy(),
            "method": "每个共同观测日重新设立一张标的与执行价相等、剩余30个自然日的欧式期权，以VIX年化值近似该期权波动率。计算时固定执行价、期限和波动率。",
            "interpretation": "标普500上涨1%时，多头看涨或看跌期权的Delta局部估计增加多少个百分点。这项标准化读数只随VIX变化，逐指数点的Gamma同时取决于标普点位。",
            "limitations": "VIX反映多执行价期权隐含的30天波动率。此模型没有逐合约报价、未平仓量或做市商头寸，不能测量市场总Gamma、对冲流量或交易方向。",
            "vintage": "使用本次冻结历史，不代表各历史日期当时已可取得这个版本。",
        },
        "coverage": {
            "cutoff": cutoff, "observations": len(points), "first_common_as_of": points[0]["date"] if points else None,
            "latest_common_as_of": latest, "latest_sp500_as_of": max(spot, default=None), "latest_vix_as_of": max(vol, default=None),
            "missing_sp500_dates": sorted(vol.keys() - spot.keys()), "missing_vix_dates": sorted(spot.keys() - vol.keys()),
            "sp500_gaps": spot_gaps, "vix_gaps": vol_gaps, "model_error_dates": model_errors,
        },
    }
