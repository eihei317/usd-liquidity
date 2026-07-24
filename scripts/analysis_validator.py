#!/usr/bin/env python3
"""Validate and atomically publish HY3 USD-liquidity analysis candidates."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


STANCE_LABELS = ["宽松", "中性偏松", "中性", "中性偏紧", "紧张"]
CONFIDENCE_LABELS = ["高", "中等", "低"]
CLAIM_TYPES = ["observed", "inference", "scenario"]
PRIORITIES = ["P0", "P1", "P2"]
SEVERITIES = ["high", "medium", "low", "info"]
RISK_TYPES = ["market", "data"]
MODULE_LABELS = ["偏松", "中性", "偏紧"]
AXIS_LABELS = ["偏松", "中性", "偏紧", "紧张", "数据不足"]
JPY_MODULE_LABELS = MODULE_LABELS + ["数据不足"]

_TEXT_SCHEMA: Dict[str, Any] = {"type": "string", "minLength": 1}
_STRING_ARRAY_SCHEMA: Dict[str, Any] = {
    "type": "array",
    "items": {"type": "string", "minLength": 1},
    "minItems": 1,
    "uniqueItems": True,
}
_CLAIM_PROPERTIES: Dict[str, Any] = {
    "claim_type": {"type": "string", "enum": CLAIM_TYPES},
    "dedupe_key": {
        "type": "string",
        "minLength": 1,
        "pattern": r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$",
    },
    "fact_ids": _STRING_ARRAY_SCHEMA,
    "condition": {"type": "string", "minLength": 1},
    "title": _TEXT_SCHEMA,
    "text": _TEXT_SCHEMA,
    "evidence": _STRING_ARRAY_SCHEMA,
    "related_indicators": _STRING_ARRAY_SCHEMA,
}
_CLAIM_REQUIRED = [
    "claim_type",
    "dedupe_key",
    "fact_ids",
    "title",
    "text",
    "evidence",
    "related_indicators",
]

ANALYSIS_JSON_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "USD Liquidity Analysis",
    "type": "object",
    "additionalProperties": False,
    "required": ["meta", "stance", "axis_assessment", "key_takeaways", "risk_flags", "narrative_blocks"],
    "properties": {
        "meta": {
            "type": "object",
            "additionalProperties": False,
            "required": ["generated_at_bjt", "data_as_of", "model", "input_freshness_note"],
            "properties": {
                "generated_at_bjt": _TEXT_SCHEMA,
                "data_as_of": {
                    "type": "string",
                    "pattern": r"^\d{4}-\d{2}-\d{2}$",
                },
                "model": _TEXT_SCHEMA,
                "input_freshness_note": _TEXT_SCHEMA,
            },
        },
        "stance": {
            "type": "object",
            "additionalProperties": False,
            "required": ["label", "confidence", "score_text", "one_liner"],
            "properties": {
                "label": {"type": "string", "enum": STANCE_LABELS},
                "confidence": {"type": "string", "enum": CONFIDENCE_LABELS},
                "score_text": _TEXT_SCHEMA,
                "one_liner": _TEXT_SCHEMA,
            },
        },
        "axis_assessment": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "funding_price",
                "liquidity_buffer",
                "treasury_pricing",
                "cross_market_transmission",
            ],
            "properties": {
                axis: {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["label", "summary", "fact_ids"],
                    "properties": {
                        "label": {"type": "string", "enum": AXIS_LABELS},
                        "summary": _TEXT_SCHEMA,
                        "fact_ids": _STRING_ARRAY_SCHEMA,
                    },
                }
                for axis in (
                    "funding_price",
                    "liquidity_buffer",
                    "treasury_pricing",
                    "cross_market_transmission",
                )
            },
        },
        "key_takeaways": {
            "type": "array",
            "minItems": 0,
            "maxItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": _CLAIM_REQUIRED,
                "properties": _CLAIM_PROPERTIES,
                "allOf": [
                    {
                        "if": {"properties": {"claim_type": {"const": "scenario"}}},
                        "then": {"required": ["condition"]},
                    }
                ],
            },
        },
        "risk_flags": {
            "type": "array",
            "minItems": 0,
            "maxItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["priority", "severity", "type"] + _CLAIM_REQUIRED,
                "properties": {
                    "priority": {"type": "string", "enum": PRIORITIES},
                    "severity": {"type": "string", "enum": SEVERITIES},
                    "type": {"type": "string", "enum": RISK_TYPES},
                    **_CLAIM_PROPERTIES,
                },
                "allOf": [
                    {
                        "if": {"properties": {"claim_type": {"const": "scenario"}}},
                        "then": {"required": ["condition"]},
                    }
                ],
            },
        },
        "narrative_blocks": {
            "type": "object",
            "additionalProperties": False,
            "required": ["treasury_yields"],
            "properties": {
                "summary": _TEXT_SCHEMA,
                "rates": _TEXT_SCHEMA,
                "balance_sheet": _TEXT_SCHEMA,
                "market_transmission": _TEXT_SCHEMA,
                "treasury_yields": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["label", "one_liner", "analysis"],
                    "properties": {
                        "label": {"type": "string", "enum": MODULE_LABELS},
                        "one_liner": _TEXT_SCHEMA,
                        "analysis": _TEXT_SCHEMA,
                    },
                },
                "jpy_carry": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["label", "one_liner", "analysis"],
                    "properties": {
                        "label": {"type": "string", "enum": JPY_MODULE_LABELS},
                        "one_liner": _TEXT_SCHEMA,
                        "analysis": _TEXT_SCHEMA,
                    },
                },
            },
        },
    },
}

_FACT_CONTAINER_KEYS = {
    "canonical_metrics",
    "derived_facts",
    "derived_signals",
    "event_facts",
    "events",
    "facts",
    "metrics",
    "quality_flags",
}
_CORE_FUNDING_PRICE_IDS = {
    "BGCR_IORB_SPREAD",
    "BGCR_PRESSURE",
    "EFFR_IORB_SPREAD",
    "EFFR_PRESSURE",
    "OBFR_IORB_SPREAD",
    "OBFR_PRESSURE",
    "REPO_PRESSURE",
    "SOFR_ANCHOR",
    "SOFR_IORB_SPREAD",
    "SOFR_PRESSURE",
    "TGCR_IORB_SPREAD",
    "TGCR_PRESSURE",
}
_EXPLICIT_BAD_STATUSES = {
    "error",
    "failed",
    "missing",
    "not_available",
    "stale",
    "unavailable",
    "unknown",
}
_PREDICTION_PATTERNS: Sequence[Tuple[str, re.Pattern[str]]] = (
    (
        "概率预测",
        re.compile(
            r"(?:大概率|高概率|较高概率|很可能|概率\s*(?:为|达到|约为)?\s*\d+(?:\.\d+)?\s*%|"
            r"\d+(?:\.\d+)?\s*%\s*(?:的)?(?:概率|可能性))",
            re.IGNORECASE,
        ),
    ),
    (
        "时间预测",
        re.compile(
            r"(?:未来|接下来|随后)?\s*\d+\s*(?:[-~—–至到]\s*\d+\s*)?"
            r"(?:个)?(?:交易日|天|周|月|季|季度|年)(?:之?内|以后|之后|后)",
            re.IGNORECASE,
        ),
    ),
    (
        "目标区间预测",
        re.compile(
            r"(?:目标(?:价|点位|区间|水平)?|预测|预计)\s*(?:为|达到|升至|降至|在)?\s*"
            r"[-+]?\d+(?:\.\d+)?\s*(?:%|bp|bps|点|美元|日元)?\s*"
            r"(?:[-~—–至到]\s*[-+]?\d+(?:\.\d+)?\s*(?:%|bp|bps|点|美元|日元)?)?",
            re.IGNORECASE,
        ),
    ),
)


def build_hy3_tool_definition() -> Dict[str, Any]:
    """Return the OpenAI-compatible HY3 function/tool definition."""
    return {
        "type": "function",
        "function": {
            "name": "submit_liquidity_analysis",
            "description": "提交只基于本次事实包、可由固定前端渲染的美元流动性结构化分析。",
            "parameters": copy.deepcopy(ANALYSIS_JSON_SCHEMA),
        },
    }


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _validate_schema(value: Any, schema: Mapping[str, Any], path: str, errors: List[str]) -> None:
    expected = schema.get("type")
    if isinstance(expected, str) and not _json_type_matches(value, expected):
        errors.append(f"{path}: 应为 {expected}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: 非法枚举值 {value!r}，允许值为 {schema['enum']}")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: 必须等于 {schema['const']!r}")

    if isinstance(value, str):
        minimum = schema.get("minLength")
        if isinstance(minimum, int) and len(value.strip()) < minimum:
            errors.append(f"{path}: 不得为空")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            errors.append(f"{path}: 格式不符合 {pattern}")

    if isinstance(value, list):
        minimum = schema.get("minItems")
        maximum = schema.get("maxItems")
        if isinstance(minimum, int) and len(value) < minimum:
            errors.append(f"{path}: 至少需要 {minimum} 项")
        if isinstance(maximum, int) and len(value) > maximum:
            errors.append(f"{path}: 最多允许 {maximum} 项")
        if schema.get("uniqueItems"):
            seen: Set[str] = set()
            for index, item in enumerate(value):
                marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if marker in seen:
                    errors.append(f"{path}[{index}]: 数组项重复")
                seen.add(marker)
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_schema(item, item_schema, f"{path}[{index}]", errors)

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}.{key}: 缺少必填字段")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}.{key}: 不允许的字段")
        for key, child_schema in properties.items():
            if key in value and isinstance(child_schema, dict):
                _validate_schema(value[key], child_schema, f"{path}.{key}", errors)


def _walk_fact_containers(
    value: Any,
    path: Tuple[str, ...],
    facts: Dict[str, Dict[str, Any]],
    duplicates: Set[str],
) -> None:
    if isinstance(value, dict):
        fact_id = value.get("fact_id")
        if not isinstance(fact_id, str) and path and path[-1] in _FACT_CONTAINER_KEYS:
            fallback_id = value.get("id")
            if isinstance(fallback_id, str):
                fact_id = fallback_id
        if isinstance(fact_id, str) and fact_id.strip():
            normalized = fact_id.strip()
            if normalized in facts and facts[normalized] is not value:
                duplicates.add(normalized)
            else:
                facts[normalized] = value
        for key, child in value.items():
            _walk_fact_containers(child, path + (str(key),), facts, duplicates)
    elif isinstance(value, list):
        container = path[-1] if path else ""
        for child in value:
            if isinstance(child, dict) and container in _FACT_CONTAINER_KEYS:
                fact_id = child.get("fact_id") or child.get("id")
                if isinstance(fact_id, str) and fact_id.strip():
                    normalized = fact_id.strip()
                    if normalized in facts and facts[normalized] is not child:
                        duplicates.add(normalized)
                    else:
                        facts[normalized] = child
            _walk_fact_containers(child, path, facts, duplicates)


def _collect_facts(model_input: Any) -> Tuple[Dict[str, Dict[str, Any]], Set[str]]:
    facts: Dict[str, Dict[str, Any]] = {}
    duplicates: Set[str] = set()
    _walk_fact_containers(model_input, (), facts, duplicates)
    return facts, duplicates


def _fact_is_fresh(fact: Mapping[str, Any]) -> bool:
    for key in ("is_fresh", "fresh"):
        if key in fact and fact[key] is False:
            return False
    if fact.get("stale") is True:
        return False
    for key in ("status", "freshness", "quality", "type"):
        status = fact.get(key)
        if isinstance(status, str) and status.strip().lower().replace(" ", "_") in _EXPLICIT_BAD_STATUSES:
            return False
    flags = fact.get("quality_flags")
    if flags:
        text = json.dumps(flags, ensure_ascii=False).lower()
        if any(token in text for token in ('"stale"', '"missing"', '"unavailable"', '"error"', "过期", "缺失")):
            return False
    if "value" in fact and fact.get("value") is None:
        kind = str(fact.get("fact_type") or fact.get("kind") or "").lower()
        if kind not in {"event", "quality", "data_quality"}:
            return False
    return True


def _is_core_funding_price(fact_id: str, fact: Mapping[str, Any]) -> bool:
    normalized = fact_id.upper().replace("-", "_").rsplit(":", 1)[-1]
    if normalized in _CORE_FUNDING_PRICE_IDS:
        return True
    if any(normalized.startswith(prefix) for prefix in ("EFFR_", "OBFR_", "SOFR_", "TGCR_", "BGCR_")):
        if any(token in normalized for token in ("ANCHOR", "IORB", "PRESSURE", "SPREAD")):
            return True
    if fact.get("is_core_funding_price") is True:
        return True
    metadata = " ".join(
        str(fact.get(key, ""))
        for key in ("p0_role", "role", "dimension", "category", "fact_type", "name")
    ).lower()
    return (
        any(token in metadata for token in ("core_funding_price", "funding_price", "资金价格", "融资价格"))
        and any(token in metadata for token in ("anomaly", "pressure", "spread", "异常", "压力", "利差"))
    )


def _parse_date(value: str) -> Optional[datetime]:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def _validate_dates(candidate: Mapping[str, Any], model_input: Mapping[str, Any], errors: List[str]) -> None:
    meta = candidate.get("meta")
    if not isinstance(meta, dict):
        return
    data_as_of = meta.get("data_as_of")
    if isinstance(data_as_of, str) and _parse_date(data_as_of) is None:
        errors.append("$.meta.data_as_of: 必须是有效的 YYYY-MM-DD 日期")
    expected_generated = model_input.get("generated_at_bjt")
    actual_generated = meta.get("generated_at_bjt")
    if isinstance(expected_generated, str) and actual_generated != expected_generated:
        errors.append("$.meta.generated_at_bjt: 必须与 model_input.generated_at_bjt 完全一致")
    if isinstance(data_as_of, str) and _parse_date(data_as_of) is not None:
        generated_date = None
        if isinstance(expected_generated, str):
            match = re.match(r"^(\d{4}-\d{2}-\d{2})", expected_generated)
            if match:
                generated_date = _parse_date(match.group(1))
        if generated_date is not None and _parse_date(data_as_of) > generated_date:
            errors.append("$.meta.data_as_of: 不得晚于本次 model_input 的生成日期")


def _iter_claims(candidate: Mapping[str, Any]) -> Iterable[Tuple[str, Mapping[str, Any]]]:
    for section in ("key_takeaways", "risk_flags"):
        items = candidate.get(section)
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            if isinstance(item, dict):
                yield f"$.{section}[{index}]", item


def _validate_axis_fact_ids(
    candidate: Mapping[str, Any], facts: Mapping[str, Mapping[str, Any]], errors: List[str]
) -> None:
    axes = candidate.get("axis_assessment")
    if not isinstance(axes, dict):
        return
    for axis_name, axis in axes.items():
        if not isinstance(axis, dict):
            continue
        fact_ids = axis.get("fact_ids")
        if not isinstance(fact_ids, list):
            continue
        for index, fact_id in enumerate(fact_ids):
            if isinstance(fact_id, str) and fact_id not in facts:
                errors.append(
                    f"$.axis_assessment.{axis_name}.fact_ids[{index}]: "
                    f"未在 model_input 事实包中找到 {fact_id!r}"
                )


def _claim_text(claim: Mapping[str, Any]) -> str:
    parts: List[str] = []
    for key in ("title", "text", "condition"):
        value = claim.get(key)
        if isinstance(value, str):
            parts.append(value)
    evidence = claim.get("evidence")
    if isinstance(evidence, list):
        parts.extend(item for item in evidence if isinstance(item, str))
    return "\n".join(parts)


_UNIT_NUMBER_PATTERN = re.compile(
    r"(?P<number>[-+]?\d[\d,]*(?:\.\d+)?)\s*(?P<unit>%|bp|bps|bn|x|口|pt)(?![A-Za-z0-9])",
    re.IGNORECASE,
)


def _iter_numeric_values(value: Any) -> Iterable[float]:
    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)):
        yield float(value)
    elif isinstance(value, dict):
        for child in value.values():
            yield from _iter_numeric_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_numeric_values(child)


def _number_matches_fact(number: float, unit: str, fact_values: Sequence[float]) -> bool:
    candidates = [number]
    if unit == "%":
        candidates.append(number / 100.0)
    for candidate in candidates:
        for fact_value in fact_values:
            tolerance = max(0.011, abs(fact_value) * 0.001)
            if abs(candidate - fact_value) <= tolerance:
                return True
    return False


def _validate_claim_numbers(
    path: str,
    claim: Mapping[str, Any],
    facts: Mapping[str, Mapping[str, Any]],
    errors: List[str],
) -> None:
    fact_ids = claim.get("fact_ids")
    if not isinstance(fact_ids, list):
        return
    referenced = [facts[fact_id] for fact_id in fact_ids if isinstance(fact_id, str) and fact_id in facts]
    fact_values = list(_iter_numeric_values(referenced))
    if not fact_values:
        return
    seen: Set[Tuple[float, str]] = set()
    for match in _UNIT_NUMBER_PATTERN.finditer(_claim_text(claim)):
        number = float(match.group("number").replace(",", ""))
        unit = match.group("unit").lower()
        marker = (number, unit)
        if marker in seen:
            continue
        seen.add(marker)
        if not _number_matches_fact(number, unit, fact_values):
            errors.append(
                f"{path}: 数值 {match.group(0)!r} 无法在所引用 fact_ids 的数值字段中追溯"
            )


def _prediction_is_supported(claim: Mapping[str, Any], facts: Mapping[str, Mapping[str, Any]]) -> bool:
    fact_ids = claim.get("fact_ids")
    if not isinstance(fact_ids, list):
        return False
    for fact_id in fact_ids:
        fact = facts.get(fact_id) if isinstance(fact_id, str) else None
        if fact and (fact.get("supports_prediction") is True or fact.get("prediction_allowed") is True):
            return True
    return False


def _validate_claims(
    candidate: Mapping[str, Any],
    facts: Mapping[str, Mapping[str, Any]],
    errors: List[str],
) -> None:
    dedupe_keys: Dict[str, str] = {}
    for path, claim in _iter_claims(candidate):
        claim_type = claim.get("claim_type")
        condition = claim.get("condition")
        if claim_type == "scenario" and (not isinstance(condition, str) or not condition.strip()):
            errors.append(f"{path}.condition: scenario 必须提供非空触发条件")
        if claim_type != "scenario" and isinstance(condition, str) and condition.strip():
            errors.append(f"{path}.condition: 仅 scenario 可以提供条件")
        if path.startswith("$.key_takeaways") and claim_type not in (None, "observed"):
            errors.append(f"{path}.claim_type: key_takeaways 只能陈述 observed 当前事实")

        dedupe_key = claim.get("dedupe_key")
        if isinstance(dedupe_key, str) and dedupe_key:
            if dedupe_key in dedupe_keys:
                errors.append(f"{path}.dedupe_key: 与 {dedupe_keys[dedupe_key]} 重复 ({dedupe_key})")
            else:
                dedupe_keys[dedupe_key] = path

        fact_ids = claim.get("fact_ids")
        if isinstance(fact_ids, list):
            for index, fact_id in enumerate(fact_ids):
                if isinstance(fact_id, str) and fact_id not in facts:
                    errors.append(f"{path}.fact_ids[{index}]: 未在 model_input 事实包中找到 {fact_id!r}")

        _validate_claim_numbers(path, claim, facts, errors)

        if not _prediction_is_supported(claim, facts):
            text = _claim_text(claim)
            for label, pattern in _PREDICTION_PATTERNS:
                match = pattern.search(text)
                if match:
                    errors.append(f"{path}: 存在无事实授权的{label} {match.group(0)!r}")


def _unfresh_fact_ids(facts: Mapping[str, Mapping[str, Any]]) -> Set[str]:
    unfresh = {fact_id for fact_id, fact in facts.items() if not _fact_is_fresh(fact)}
    for fact in facts.values():
        fact_type = str(fact.get("type") or "").lower()
        if fact_type not in _EXPLICIT_BAD_STATUSES:
            continue
        metric_id = fact.get("metric_id")
        signal_id = fact.get("signal_id")
        event_fact_id = fact.get("event_fact_id")
        if isinstance(metric_id, str):
            unfresh.add(f"metric:{metric_id.upper()}")
        if isinstance(signal_id, str):
            unfresh.add(f"derived:{signal_id.upper()}")
        if isinstance(event_fact_id, str):
            unfresh.add(event_fact_id)
    changed = True
    while changed:
        changed = False
        for fact_id, fact in facts.items():
            base_ids = fact.get("base_fact_ids")
            if fact_id not in unfresh and isinstance(base_ids, list) and any(base_id in unfresh for base_id in base_ids):
                unfresh.add(fact_id)
                changed = True
    return unfresh


def _risk_is_funding_pressure(risk: Mapping[str, Any]) -> bool:
    identifiers: List[str] = []
    for key in ("fact_ids", "related_indicators"):
        values = risk.get(key)
        if isinstance(values, list):
            identifiers.extend(str(value).upper() for value in values)
    text = " ".join(str(risk.get(key, "")) for key in ("title", "text"))
    return (
        any(token in identifier for identifier in identifiers for token in ("SOFR", "EFFR", "OBFR", "TGCR", "BGCR", "REPO"))
        or any(token in text for token in ("资金价格", "融资价格", "回购融资", "银行间融资"))
    )


def _validate_p0(
    candidate: Mapping[str, Any],
    facts: Mapping[str, Mapping[str, Any]],
    errors: List[str],
) -> None:
    risk_flags = candidate.get("risk_flags")
    if not isinstance(risk_flags, list):
        return
    order = {priority: index for index, priority in enumerate(PRIORITIES)}
    unfresh = _unfresh_fact_ids(facts)
    previous = -1
    for index, risk in enumerate(risk_flags):
        if not isinstance(risk, dict):
            continue
        priority = risk.get("priority")
        if priority in order:
            current = order[priority]
            if current < previous:
                errors.append(f"$.risk_flags[{index}].priority: risk_flags 必须按 P0、P1、P2 排序")
            previous = max(previous, current)
        if priority != "P0":
            continue
        path = f"$.risk_flags[{index}]"
        if risk.get("type") != "market":
            errors.append(f"{path}.type: P0 只能是已实现的 market 压力，不能是 data 风险")
        if risk.get("severity") != "high":
            errors.append(f"{path}.severity: P0 必须为 high")
        fact_ids = risk.get("fact_ids")
        if not isinstance(fact_ids, list):
            continue
        usable: List[Tuple[str, Mapping[str, Any]]] = []
        for fact_id in fact_ids:
            fact = facts.get(fact_id) if isinstance(fact_id, str) else None
            if fact is not None:
                if fact_id in unfresh:
                    errors.append(f"{path}.fact_ids: P0 不得引用不新鲜或缺失事实 {fact_id!r}")
                else:
                    usable.append((fact_id, fact))
        if len({fact_id for fact_id, _ in usable}) < 2:
            errors.append(f"{path}.fact_ids: P0 至少需要两个不同的新鲜事实交叉确认")
        if (
            _risk_is_funding_pressure(risk)
            and usable
            and not any(_is_core_funding_price(fact_id, fact) for fact_id, fact in usable)
        ):
            errors.append(f"{path}.fact_ids: 融资压力 P0 必须包含至少一个核心资金价格异常事实")


def _has_jpy_input(model_input: Mapping[str, Any]) -> bool:
    data = model_input.get("data")
    if not isinstance(data, dict):
        data = model_input
    containers = [data]
    facts = data.get("facts")
    if isinstance(facts, dict):
        containers.append(facts)
    for container in containers:
        for key in ("jpy_carry", "jpy_carry_facts", "jpy_carry_history"):
            value = container.get(key)
            if isinstance(value, dict) and value:
                return True
    return False


def _validate_required_modules(
    candidate: Mapping[str, Any], model_input: Mapping[str, Any], errors: List[str]
) -> None:
    if not _has_jpy_input(model_input):
        return
    narratives = candidate.get("narrative_blocks")
    if isinstance(narratives, dict) and "jpy_carry" not in narratives:
        errors.append("$.narrative_blocks.jpy_carry: model_input 含 JPY carry 事实时必须输出该模块")


def _iter_narrative_strings(value: Any, path: str) -> Iterable[Tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from _iter_narrative_strings(child, f"{path}.{key}")


def _validate_uncited_predictions(candidate: Mapping[str, Any], errors: List[str]) -> None:
    for root_key in ("stance", "narrative_blocks"):
        value = candidate.get(root_key)
        for path, text in _iter_narrative_strings(value, f"$.{root_key}"):
            for label, pattern in _PREDICTION_PATTERNS:
                match = pattern.search(text)
                if match:
                    errors.append(f"{path}: 不带 fact_ids 的区域不得包含{label} {match.group(0)!r}")


def validate_analysis(candidate: Any, model_input: Any) -> List[str]:
    """Return validation errors; an empty list means the candidate is publishable."""
    errors: List[str] = []
    _validate_schema(candidate, ANALYSIS_JSON_SCHEMA, "$", errors)
    if not isinstance(candidate, dict):
        return errors
    if not isinstance(model_input, dict):
        errors.append("model_input: 应为 object")
        return errors

    facts, duplicates = _collect_facts(model_input)
    for fact_id in sorted(duplicates):
        errors.append(f"model_input: fact_id 重复 {fact_id!r}")
    _validate_dates(candidate, model_input, errors)
    _validate_claims(candidate, facts, errors)
    _validate_p0(candidate, facts, errors)
    _validate_required_modules(candidate, model_input, errors)
    _validate_uncited_predictions(candidate, errors)
    return errors


def _load_json(path: Path, label: str) -> Tuple[Optional[Any], List[str]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle), []
    except FileNotFoundError:
        return None, [f"{label}: 文件不存在: {path}"]
    except json.JSONDecodeError as exc:
        return None, [f"{label}: JSON 解析失败（第 {exc.lineno} 行第 {exc.colno} 列）: {exc.msg}"]
    except OSError as exc:
        return None, [f"{label}: 读取失败: {exc}"]


def validate_analysis_files(candidate_path: os.PathLike[str] | str, model_input_path: os.PathLike[str] | str) -> List[str]:
    candidate, candidate_errors = _load_json(Path(candidate_path), "candidate")
    model_input, input_errors = _load_json(Path(model_input_path), "model_input")
    errors = candidate_errors + input_errors
    if errors:
        return errors
    return validate_analysis(candidate, model_input)


def _atomic_write_json(payload: Any, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_temp_path = tempfile.mkstemp(
        prefix=f".{output_path.name}.", suffix=".tmp", dir=str(output_path.parent)
    )
    temp_path = Path(raw_temp_path)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, output_path)
        try:
            directory_fd = os.open(str(output_path.parent), os.O_RDONLY)
        except OSError:
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        temp_path.unlink(missing_ok=True)


def publish_analysis_candidate(
    candidate_path: os.PathLike[str] | str,
    output_path: os.PathLike[str] | str,
    model_input_path: os.PathLike[str] | str,
) -> List[str]:
    """Validate candidate_path and atomically replace output_path only on success."""
    candidate, candidate_errors = _load_json(Path(candidate_path), "candidate")
    model_input, input_errors = _load_json(Path(model_input_path), "model_input")
    errors = candidate_errors + input_errors
    if not errors:
        errors.extend(validate_analysis(candidate, model_input))
    if errors:
        return errors
    try:
        _atomic_write_json(candidate, Path(output_path))
    except (OSError, TypeError, ValueError) as exc:
        return [f"publish: 原子写入失败: {exc}"]
    return []


def _resolve_cli_path(positional: Optional[str], option: Optional[str], parser: argparse.ArgumentParser, name: str) -> str:
    value = option or positional
    if not value:
        parser.error(f"缺少 {name} 路径")
    return value


def parse_args(argv: Sequence[str]) -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    parser = argparse.ArgumentParser(description="校验或原子发布 HY3 美元流动性 analysis.json")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="只校验候选 JSON")
    validate_parser.add_argument("candidate_pos", nargs="?", help="候选 analysis JSON")
    validate_parser.add_argument("--candidate", dest="candidate_opt", help="候选 analysis JSON")
    validate_parser.add_argument("--model-input", required=True, help="本次 model_input JSON")

    publish_parser = subparsers.add_parser("publish", help="校验通过后原子发布")
    publish_parser.add_argument("candidate_pos", nargs="?", help="候选 analysis JSON")
    publish_parser.add_argument("output_pos", nargs="?", help="发布目标 analysis JSON")
    publish_parser.add_argument("--candidate", dest="candidate_opt", help="候选 analysis JSON")
    publish_parser.add_argument("--output", dest="output_opt", help="发布目标 analysis JSON")
    publish_parser.add_argument("--model-input", required=True, help="本次 model_input JSON")
    return parser, parser.parse_args(list(argv))


def main(argv: Sequence[str]) -> int:
    parser, args = parse_args(argv)
    candidate_path = _resolve_cli_path(args.candidate_pos, args.candidate_opt, parser, "candidate")
    if args.command == "validate":
        errors = validate_analysis_files(candidate_path, args.model_input)
        status = "valid" if not errors else "validation_failed"
        print(json.dumps({"status": status, "errors": errors}, ensure_ascii=False, indent=2))
        return 0 if not errors else 2

    output_path = _resolve_cli_path(args.output_pos, args.output_opt, parser, "output")
    errors = publish_analysis_candidate(candidate_path, output_path, args.model_input)
    status = "published" if not errors else "validation_failed"
    payload: Dict[str, Any] = {"status": status, "errors": errors}
    if not errors:
        payload["output"] = str(Path(output_path).resolve())
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
