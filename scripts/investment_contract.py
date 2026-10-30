"""Investment research schema and checks, separate from a trading recommendation."""
from __future__ import annotations

import re

TEXT = {"type": "string", "minLength": 1}
REFS = {"type": "array", "items": TEXT, "minItems": 1, "uniqueItems": True}


def obj(properties):
    return {"type": "object", "additionalProperties": False,
            "required": list(properties), "properties": properties}


ASSET = obj({
    "liquidity_bias": {"type": "string", "enum": ["支持", "中性", "压制", "分化", "数据不足"]},
    "confidence": {"type": "string", "enum": ["高", "中等", "低"]},
    "horizon": {"type": "string", "enum": ["2—4周", "1—3个月", "2—12周"]},
    **{key: TEXT for key in ("summary", "transmission", "confirmation", "invalidation", "coverage_limits")},
    "fact_ids": REFS,
})
SCENARIO = obj({"path": TEXT, "trigger": TEXT, "invalidation": TEXT, "fact_ids": REFS})
INVESTMENT_SCHEMA = obj({
    "summary": TEXT,
    "change_summary": TEXT,
    "equities": ASSET,
    "bitcoin": ASSET,
    "expectations": obj({
        "status": {"type": "string", "enum": ["已覆盖", "部分覆盖", "数据不足"]},
        "summary": TEXT, "fact_ids": REFS,
    }),
    "scenarios": obj({name: SCENARIO for name in ("base", "upside", "downside")}),
    "next_checks": {"type": "array", "minItems": 1, "maxItems": 5, "items": TEXT},
})

# Financing conditions and discount rates are drivers. Asset prices, VIX and
# credit spreads are confirmation and never create independent upstream votes.
DRIVERS = {"SOFR", "IORB", "EFFR", "OBFR", "TGCR", "BGCR", "TGA", "RRPONTSYD",
           "WRESBAL", "SOMA", "SRP_ACCEPTED", "DGS1", "DGS3", "DGS5", "DGS7",
           "DFII5", "DFII7", "DFII10", "FRBSF_EXPECTED_SHORT_2Y",
           "FRBSF_EXPECTED_SHORT_10Y", "FRBSF_TERM_PREMIUM_2Y", "FRBSF_TERM_PREMIUM_10Y"}
DRIVER_GROUPS = {
    "funding": {"SOFR", "EFFR", "OBFR", "TGCR", "BGCR", "SRP_ACCEPTED"},
    "quantity": {"TGA", "RRPONTSYD", "WRESBAL", "SOMA"},
    "discount": {"DGS1", "DGS3", "DGS5", "DGS7", "DFII5", "DFII7", "DFII10",
                 "FRBSF_EXPECTED_SHORT_2Y", "FRBSF_EXPECTED_SHORT_10Y",
                 "FRBSF_TERM_PREMIUM_2Y", "FRBSF_TERM_PREMIUM_10Y"},
}


def _strings(value, path="investment_assessment"):
    if isinstance(value, dict):
        for key, child in value.items():
            if key != "fact_ids":
                yield from _strings(child, path + "." + key)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from _strings(child, path + f"[{i}]")
    elif isinstance(value, str):
        yield path, value


def _roots(fid, facts, seen=None):
    seen = set() if seen is None else seen
    if fid in seen:
        return set()
    seen.add(fid)
    fact = facts.get(fid, {})
    parents = fact.get("base_fact_ids", [])
    if parents:
        return set().union(*(_roots(p, facts, seen.copy()) for p in parents))
    return {fid.split(":", 1)[-1]}


def validate_investment(candidate, package, facts, unfresh=None):
    errors = []
    unfresh = set() if unfresh is None else unfresh
    value = candidate.get("investment_assessment")
    if not isinstance(value, dict):
        if package.get("research_version") == "3.0":
            errors.append("$.investment_assessment: 本版必须包含投资研究")
        return errors

    def check_refs(item, path):
        refs = item.get("fact_ids", [])
        if not isinstance(refs, list):
            return []
        for fid in refs:
            if isinstance(fid, str) and fid not in facts:
                errors.append(path + ": 未找到事实 " + fid)
        return [fid for fid in refs if isinstance(fid, str) and fid in facts]

    for key in ("equities", "bitcoin"):
        item = value.get(key, {})
        if not isinstance(item, dict):
            continue
        refs = check_refs(item, "investment_assessment." + key)
        valid = [fid for fid in refs if fid not in unfresh and facts[fid].get("status", "ok") == "ok"
                 and facts[fid].get("is_fresh") is not False
                 and not facts[fid].get("stale")]
        upstream = [fid for fid in valid if _roots(fid, facts) & DRIVERS]
        if item.get("liquidity_bias") != "数据不足" and not upstream:
            errors.append(f"investment_assessment.{key}: 流动性判断须引用可用的上游资金或折现率事实，市场反应不能替代")
        if item.get("confidence") == "高":
            trends = [fid for fid in upstream if fid.startswith("trend:")
                      and facts[fid].get("window_observations", 0) >= 5]
            independent = set().union(*(_roots(fid, facts) for fid in trends)) if trends else set()
            groups = {group for group, ids in DRIVER_GROUPS.items() if independent & ids}
            if len(trends) < 2 or len(groups) < 2:
                errors.append(f"investment_assessment.{key}: 高置信度缺少两个独立机制的多期证据；政策锚和同曲线期限不能重复投票")
        if item.get("liquidity_bias") == "数据不足" and item.get("confidence") == "高":
            errors.append(f"investment_assessment.{key}: 数据不足不能给高置信度")

    expectation = value.get("expectations", {})
    if isinstance(expectation, dict):
        refs = check_refs(expectation, "investment_assessment.expectations")
        if expectation.get("status") == "已覆盖" and not any(
            facts[fid].get("measurement_type") in {"direct_market_pricing", "survey"}
            and fid not in unfresh and facts[fid].get("status", "ok") == "ok"
            and facts[fid].get("is_fresh") is not False and not facts[fid].get("stale") for fid in refs
        ):
            errors.append("investment_assessment.expectations: 已覆盖须有直接市场定价或调查事实；模型分解和价格反应不足以证明市场预期")

    scenarios = value.get("scenarios", {})
    if isinstance(scenarios, dict):
        for key, scenario in scenarios.items():
            if not isinstance(scenario, dict):
                continue
            check_refs(scenario, "investment_assessment.scenarios." + key)
            trigger, invalidation = scenario.get("trigger", ""), scenario.get("invalidation", "")
            if isinstance(trigger, str) and trigger.strip() == str(invalidation).strip():
                errors.append("investment_assessment.scenarios." + key + ": 触发与失效条件不得相同")
    for path, text in _strings(value):
        if re.search(r"[-+]?\d[\d,.]*\s*(?:%|bps?\b|bn\b|mn\b|美元|日元|指数点|倍)", text, re.I):
            errors.append(path + ": 数值必须通过事实表呈现，禁止手抄市场数字或编造目标/概率/仓位")
        if re.search(r"必涨|必跌|稳赚|保证收益|确定上涨|确定下跌", text):
            errors.append(path + ": 不得作确定收益承诺")
    return errors
