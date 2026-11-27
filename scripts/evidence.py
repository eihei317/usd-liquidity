"""Render captured facts for readers without changing their units or observation windows."""
import math
import re

from .utils import RATE_LABELS


_LABELS = {
    "iv_minus_rv21": "标普500隐含与已实现波动率之差",
    "option_oi_share": "标普500股指期货市场的期权未平仓量占比",
    "SRP_ACCEPTED": "常备回购工具用量", "SRP_RATE": "常备回购工具利率",
    "SP500": "标普500指数", "NASDAQCOM": "纳斯达克综合指数", "CBBTCUSD": "比特币美元价格",
    "CFTC_JPY_NET_OI": "日元期货非商业净持仓占未平仓量的比例",
    "CFTC_JPY_GROSS_LONG": "日元期货非商业多头持仓", "CFTC_JPY_GROSS_SHORT": "日元期货非商业空头持仓",
    "CFTC_JPY_SHORT_SHARE": "日元期货非商业空头占比", "CFTC_JPY_OPEN_INTEREST": "日元期货未平仓量",
    "USDJPY": "美元兑日元", "USDJPY_VOL20": "美元兑日元20期年化波动率",
    "US_JP_2Y": "美日两年期国债利差", "US_JP_10Y": "美日十年期国债利差",
    "JPY_CALL": "日元隔夜拆借利率", "JPY_NEER": "日元名义有效汇率",
}
JPY_UNITS = {
    "USDJPY": "JPY per USD", "USDJPY_VOL20": "%", "US_JP_2Y": "bp", "US_JP_10Y": "bp",
    "JPY_CALL": "%", "JGB2": "%", "JGB5": "%", "JGB10": "%", "JGB30": "%", "JPY_NEER": "index",
    "CFTC_JPY_NET_OI": "net/OI", "CFTC_JPY_SHORT_SHARE": "short/(short+long)",
    "CFTC_JPY_GROSS_SHORT": "contracts", "CFTC_JPY_GROSS_LONG": "contracts", "CFTC_JPY_OPEN_INTEREST": "contracts",
}
_UNITS = {
    "波动率点": (1, "个波动率点"),
    "USD bn": (10, "亿美元"), "bn": (10, "亿美元"), "USD mn/day": (1, "百万美元/日"),
    "contracts": (1, "手"), "JPY per USD": (1, "日元/美元"), "USD": (1, "美元"),
    "pt": (1, "点"), "index": (1, "点"), "x": (1, "倍"), "ratio": (1, "倍"),
    "bp": (1, "基点"), "bp avg": (1, "基点"), "%": (1, "%"),
}


def _number(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def _quantity(value, unit, *, change=False):
    scale, label = _UNITS.get(unit, (1, unit))
    if unit in {"fraction", "net/OI", "short/(short+long)"}:
        scale, label = 100, "个百分点" if change else "%"
    elif unit == "%" and change:
        scale, label = 100, "基点"
    scaled = value * scale
    # Keep small observations visible, while suppressing floating-point subtraction noise.
    decimals = 2 if abs(scaled) >= 0.01 or scaled == 0 else min(8, 1 - math.floor(math.log10(abs(scaled))))
    rounded = round(scaled, decimals) or 0
    text = f"{rounded:,.{decimals}f}".rstrip("0").rstrip(".")
    return f"{text}{label}"


def _label(fact, mid):
    if mid == "SOFR_ANCHOR":
        deps = fact.get("base_fact_ids") or []
        if any(key in deps for key in ("metric:DFEDTARU", "metric:POLICY_UPPER_NYFED")):
            return "担保隔夜融资利率与联邦基金目标上限之差"
        if "IORB" in (fact.get("name") or ""):
            return "担保隔夜融资利率与准备金利率之差"
        return "担保隔夜融资利率与政策基准之差"
    name = _LABELS.get(mid) or RATE_LABELS.get(mid) or fact.get("name") or mid
    name = name.split("：", 1)[0].removesuffix("较上次成功事实包")
    return re.sub(r"^[^（]*[A-Za-z][^（]*（(.+)）$", r"\1", name)


def _event_evidence(fact):
    parts = []
    if fact.get("announcement_date"):
        parts.append(f"{fact['announcement_date']} 公告")
    if fact.get("auction_date"):
        parts.append(f"{fact['auction_date']} 拍卖")
    if fact.get("issue_date"):
        parts.append(f"{fact['issue_date']} 发行")
    security_type = fact.get("security_type") or ""
    security_type = {"Bill": "国库券", "Note": "中期国债", "Bond": "长期国债"}.get(security_type, security_type)
    term = re.sub(r"(\d+)-(Week|Year|Day|Month)", lambda m: m[1] + {"Week": "周", "Year": "年", "Day": "天", "Month": "个月"}[m[2]], str(fact.get("security_term") or ""))
    security = (term + security_type).strip()
    if security:
        parts.append(security)
    amount = fact.get("gross_announced_offering_usd_bn")
    parts.append("已公告发行总额" + _quantity(amount, "USD bn") if _number(amount) else "发行金额待公布")
    return "，".join(parts) + "。"


def _calendar_evidence(fact):
    captured = fact.get("as_of") or "未知日期"
    start, end = fact.get("window_start") or captured, fact.get("window_end") or "未知日期"
    count, unknown = fact.get("event_count"), fact.get("unknown_amount_count")
    amount, net = fact.get("gross_announced_offering_usd_bn"), fact.get("net_cash_impact_usd_bn")
    parts = [f"截至{captured}，{start} 至 {end} 结算的已公告发行"]
    if isinstance(count, int):
        parts[0] += f"有{count}笔"
    parts.append("已知发行毛额合计" + _quantity(amount, "USD bn") if _number(amount) else "发行毛额未知")
    if unknown:
        parts.append(f"其中{unknown}笔金额待公布")
    parts.append("净筹资额为" + _quantity(net, "USD bn") if _number(net) else "净筹资额未知")
    return "，".join(parts) + "。"


_OPTION_NAMES = {
    "option:SPX:model_delta_change_1pct": "标普500的30天平值期权模型",
    "option:SPX:iv_minus_rv21": "标普500隐含与已实现波动率之差",
    "option:SP500_FUTURES:dealer_option_delta": "标普500股指期货期权的交易商方向敞口",
    "option:SP500_FUTURES:option_oi_share": "期权占标普500期货市场总未平仓量的比例（期货等值）",
    "option:SPX:gross_gamma_1pct": "SPX 与 SPXW 全部未平仓合约的 Gamma 敞口",
    "option:SPX:gamma_share_7d": "7日内到期合约占总 Gamma 敞口的比例",
    "option:SPX:gamma_share_0dte": "当日到期且仍可交易的合约占总 Gamma 敞口的比例",
}


def _gamma_money(value):
    if value >= 100_000_000:
        return _quantity(value / 100_000_000, "亿美元")
    if value >= 10_000:
        return _quantity(value / 10_000, "万美元")
    return _quantity(value, "美元")


def _option_reference(fact, window, unit):
    ref = fact.get("reference") or {}
    count = ref.get("count")
    if type(count) is not int or ref.get("window") != window:
        return ""
    if 0 <= count < window:
        return f"此前只有{count}期可比观测，尚未满{window}期。"
    start, end, percentile, high = (ref.get(key) for key in ("start", "end", "percentile", "high"))
    if count != window or not start or not end or not start <= end < (fact.get("as_of") or ""):
        return ""
    if not _number(percentile) or not 0 <= percentile <= 100 or not _number(high):
        return ""
    return (f"从{start}至{end}的前{window}期观测（不含本期）中，"
            f"{_quantity(percentile, '%')}的读数不高于本期，窗口内最高为{_quantity(high, unit)}。")


def _option_evidence(fact, fid):
    name, value = _OPTION_NAMES[fid], fact.get("value")
    status = fact.get("status")
    if status == "redistribution_unconfirmed":
        return f"{name}向指定仓库导出的权限尚未确认。"
    if not _number(value) or status in {"missing", "partial", "invalid", "unavailable_at_cutoff", "not_configured"}:
        return f"{name}本期缺少可用观测。"
    previous_date, change = fact.get("previous_as_of"), fact.get("change")
    change_unit = "个百分点"
    reference = ""
    if fid.endswith(":model_delta_change_1pct"):
        statement = f"{name}估算，指数上涨1%时，期权 Delta 约增加{_quantity(value, '个百分点')}"
    elif fid.endswith(":iv_minus_rv21"):
        change_unit = "个波动率点"
        statement = f"{name}为{_quantity(value, change_unit)}"
        if _number(fact.get("vix_pct")) and _number(fact.get("realized_vol_pct")):
            statement += (f"（VIX 为{_quantity(fact['vix_pct'], '%')}，前21个交易日收益率的"
                          f"年化波动率为{_quantity(fact['realized_vol_pct'], '%')}）")
        reference = _option_reference(fact, 252, change_unit)
    elif fid.endswith(":option_oi_share"):
        statement = f"{name}为{_quantity(value, '%')}"
        if _number(fact.get("combined_oi")) and _number(fact.get("futures_only_oi")):
            statement += (f"（CFTC 合并报表总持仓{_quantity(fact['combined_oi'], '手期货等值')}，"
                          f"仅期货报表总持仓{_quantity(fact['futures_only_oi'], '手')}）")
        reference = _option_reference(fact, 52, "%")
    elif fid.endswith(":dealer_option_delta"):
        position = "净多" if value > 0 else "净空" if value < 0 else "净额为"
        statement = f"CFTC 持仓折算显示，{name}{position}{_quantity(abs(value), '手期货等值')}"
        change_unit = "手期货等值"
    elif fid.endswith(":gross_gamma_1pct"):
        statement = f"按指数变动1%估算，{name}按绝对值合计{_gamma_money(value)}"
    else:
        statement = f"{name}为{_quantity(value, '%')}"
    if previous_date and _number(change):
        magnitude = _gamma_money(abs(change)) if fid.endswith(":gross_gamma_1pct") else _quantity(abs(change), change_unit)
        if change and fid.endswith(":dealer_option_delta"):
            direction = "多头" if change > 0 else "空头"
            statement += f"，净敞口较{previous_date}向{direction}方向变化{magnitude}"
        else:
            movement = "持平" if change == 0 else ("增加" if change > 0 else "减少") + magnitude
            statement += f"，较{previous_date}的读数{movement}"
    text = (fact.get("as_of") or "观测日期未知") + "，" + statement + "。"
    if status == "partial_latest":
        text += "最新一期的来源未能配对，以上为最近一次可比观测。"
    return text + reference


def _describe_fact(fact):
    fid = str(fact.get("fact_id", ""))
    mid = str(fact.get("id") or fid.rsplit(":", 1)[-1])
    if fid in _OPTION_NAMES:
        return _option_evidence(fact, fid)
    if fid.startswith("calendar:"):
        return _calendar_evidence(fact)
    if fid.startswith("event:"):
        return _event_evidence(fact)
    value = fact.get("value")
    if not _number(value):
        text = fact.get("message") or fact.get("text") or f"{_label(fact, mid)}缺少可用观测。"
        if fid.startswith("quality:") and fact.get("metric_id"):
            label = _label(fact, fact["metric_id"])
            observed = f"最近观测日为{fact['as_of']}。" if fact.get("as_of") else ""
            return f"{label}。{observed}{text}"
        if fid == "jpy:CFTC_DECOMPOSITION" and fact.get("as_of"):
            return f"{fact['as_of']} 当周，{text}"
        return text
    name = _label(fact, mid)
    unit = fact.get("unit") or JPY_UNITS.get(mid) or {"VIX_RISK": "index", "NFCI_LEVEL": "index"}.get(mid, "")
    end = fact.get("window_end") or fact.get("as_of")
    start = fact.get("window_start") or fact.get("previous_as_of") or fact.get("comparison_as_of_1d")
    window = fact.get("window_label")
    span = f"{start} 至 {end}" if start and end else (end or "观测日期未知")
    if fact.get("measurement") == "price_return":
        return f"{span}，{name}{'（' + window + '）' if window else ''}累计价格涨跌幅为{_quantity(value, '%')}。"
    previous, change = fact.get("previous"), fact.get("change", fact.get("change_1d"))
    if not _number(previous) and start and _number(fact.get("change_1d")):
        previous = value - fact["change_1d"]
    current = _quantity(value, unit)
    change_unit = "个百分点" if fid == "comparison:option_oi_share" else unit
    if fid.startswith("comparison:"):
        captured = str(fact.get("previous_package_generated_at_bjt") or "")[:10]
        reference = f"上次报告（{captured}）" if captured else "上次报告"
        if start and start == end and _number(change) and change == 0:
            return f"{name}沿用{end}的观测值{current}，与{reference}相同。"
        if start and start == end and _number(previous) and _number(change) and change != 0:
            move = "上修" if change > 0 else "下修"
            return (f"对比{reference}，{end}的{name}从{_quantity(previous, unit)}修订为{current}，"
                    f"{move}{_quantity(abs(change), change_unit, change=True)}。")
        name += f"（较{captured}报告）" if captured else "（较上次报告）"
    if _number(previous) and start and end:
        if start == end and not fid.startswith("comparison:"):
            return f"{end}，{name}为{current}。"
        interval = f"（{window}）" if window else ""
        if previous == value:
            text = f"{span}，{name}{interval}维持在{current}"
        else:
            text = f"{span}，{name}{interval}从{_quantity(previous, unit)}变为{current}"
            if _number(change):
                text += f"，{'增加' if change > 0 else '减少'}{_quantity(abs(change), change_unit, change=True)}"
    else:
        text = f"{end + '，' if end else ''}{name}为{current}"
        if _number(change):
            text += f"，较前一观测{'增加' if change >= 0 else '减少'}{_quantity(abs(change), change_unit, change=True)}"
    return text + "。"


def format_fact_evidence(fact):
    """Describe a cited observation and disclose the freshness of its source."""
    text = _describe_fact(fact)
    statuses = {str(fact.get(key, "")).lower() for key in ("status", "source_status", "previous_source_status")}
    if any("fail" in flag or "cached" in flag or flag == "error" for flag in statuses):
        return text + "本次或对照期来源抓取失败，所列为已留存记录。"
    if fact.get("stale") is True or "stale" in statuses:
        return text + "该观测已过期。"
    return text
