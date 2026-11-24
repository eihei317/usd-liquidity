"""Create the reader's daily view from one frozen analysis and its own facts."""
from scripts.evidence import format_fact_evidence
from scripts.investment_review import BJT, _timestamp


def _valid_comparison_dates(row, capture):
    try:
        previous = _timestamp(row.get("previous_package_generated_at_bjt"))
    except ValueError:
        return False
    start, end = row.get("previous_as_of"), row.get("as_of")
    return bool(capture and previous < capture and start and end and start <= end
                and start <= previous.astimezone(BJT).date().isoformat()
                and end <= capture.astimezone(BJT).date().isoformat())


def _first_changed_comparison(references, catalog, usable, seen):
    # Prefer explicitly cited changes over comparisons for supporting indicators.
    direct = [key for key in references if key.startswith("comparison:")]
    for key in direct + references:
        fact = catalog.get(key, {})
        for ref in [key, *fact.get("base_fact_ids", [])]:
            family, _, tail = ref.partition(":")
            if family not in ("metric", "comparison", "trend", "market"):
                continue
            indicator = tail.partition(":")[0]
            row = usable.get(indicator)
            if row and indicator not in seen and row["change"] != 0:
                return row
    return None


def _brief_evidence(analysis, research, catalog, usable):
    if "change_fact_ids" in research:
        by_id = {row["fact_id"]: row for row in usable.values()}
        rows = [by_id[fid] for fid in dict.fromkeys(research["change_fact_ids"]) if fid in by_id][:4]
    else:
        # Older analyses linked observations but did not link their change summary.
        rows = []
        seen = set()
        for claim in analysis.get("key_takeaways", []):
            row = _first_changed_comparison(claim.get("fact_ids", []), catalog, usable, seen)
            if row:
                rows.append(row)
                seen.add(row["id"])
            if len(rows) == 4:
                break
    return [{"fact_id": row["fact_id"], "text": format_fact_evidence(row)} for row in rows]


def build_daily_brief(analysis, investment):
    research = analysis.get("investment_assessment") or {}
    stance = analysis.get("stance") or {}
    catalog = investment.get("catalog", {})
    comparisons = investment.get("comparison_facts", [])
    generated = analysis.get("meta", {}).get("generated_at_bjt", "")
    try:
        capture = _timestamp(generated)
    except ValueError:
        capture = None
    usable = {
        row["id"]: row for row in comparisons
        if row.get("status") == "ok" and row.get("source_status", "ok") == "ok"
        and row.get("previous_source_status", "ok") == "ok" and row.get("previous") is not None
        and row.get("value") is not None and row.get("change") is not None
        and _valid_comparison_dates(row, capture)
    }
    unchanged = bool(usable) and all(row.get("comparison_kind") == "unchanged" for row in usable.values())
    comparison = research.get("change_summary", "")
    if unchanged and "change_fact_ids" not in research:
        comparison = "与上次快照可直接比较的有效指标，观测日期和数值均未变化。"
    elif not usable:
        comparison = "本期没有可直接比较的上次快照数据。"

    assets = []
    for key, name in (("equities", "美股"), ("bitcoin", "BTC")):
        asset = research.get(key)
        if asset:
            assets.append({"name": name, "bias": asset.get("liquidity_bias", ""), "horizon": asset.get("horizon", ""),
                           "confidence": asset.get("confidence", ""), "summary": asset.get("summary", "")})
    return {
        "date": generated,
        "stance": stance.get("label", ""), "confidence": stance.get("confidence", ""),
        "headline": stance.get("one_liner") or stance.get("summary", ""),
        "comparison": comparison, "evidence": _brief_evidence(analysis, research, catalog, usable), "assets": assets,
        "watch": next(iter(research.get("next_checks") or []), ""),
        "alerts": [row["text"] + (" 触发条件：" + row["condition"] if row.get("condition") else "")
                   for row in analysis.get("risk_flags", []) if row.get("priority") == "P0" and row.get("text")],
    }


def brief_markdown(brief):
    heading = "美元流动性日报" + (" · " + brief["stance"] if brief["stance"] else "")
    date = " · ".join(filter(None, [brief["date"], "置信度" + brief["confidence"] if brief["confidence"] else ""]))
    lines = ["# " + heading, "", date, "", brief["headline"]]
    if brief["alerts"]:
        lines += ["", "## 当前风险", "", *("- " + alert for alert in brief["alerts"])]
    lines += ["", "## 比上次有什么变化", "", brief["comparison"]]
    if brief["evidence"]:
        lines += ["", *("- " + item["text"] for item in brief["evidence"])]
    if brief["assets"]:
        lines += ["", "## 对美股和 BTC 的影响", ""]
        for asset in brief["assets"]:
            context = "，".join(filter(None, [asset["horizon"], asset["bias"], "置信度" + asset["confidence"] if asset["confidence"] else ""]))
            lines.append(f"- **{asset['name']}**{'（' + context + '）' if context else ''}{asset['summary']}")
    if brief["watch"]:
        lines += ["", "## 接下来观察", "", brief["watch"]]
    lines += ["", "[查看完整看板、趋势、判断失效条件与历史覆盖](dashboard.html)"]
    return "\n".join(lines) + "\n"
