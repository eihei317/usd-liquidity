#!/usr/bin/env python3
"""Validate and atomically publish HY3 USD-liquidity analysis candidates."""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


STANCE_LABELS = ["宽松", "中性偏松", "中性", "中性偏紧", "紧张", "数据不足"]
CONFIDENCE_LABELS = ["高", "中等", "低"]
CLAIM_TYPES = ["observed", "inference", "scenario"]
PRIORITIES = ["P0", "P1", "P2"]
SEVERITIES = ["high", "medium", "low", "info"]
RISK_TYPES = ["market", "data"]
MODULE_LABELS = ["偏松", "中性", "偏紧", "数据不足"]
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
    "evidence_refs": {"type":"array","minItems":1,"items":{"type":"object","additionalProperties":False,"required":["fact_id"],"properties":{"fact_id":{"type":"string"}}}},
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
    "evidence_refs",
]

ANALYSIS_JSON_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "USD Liquidity Analysis",
    "type": "object",
    "additionalProperties": False,
    "required": ["meta", "stance", "axis_assessment", "horizon_assessment", "key_takeaways", "risk_flags", "narrative_blocks"],
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
                        "confidence": {"type":"string","enum":CONFIDENCE_LABELS},
                        "coverage_limits": _TEXT_SCHEMA,
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
        "horizon_assessment": {
            "type": "object",
            "additionalProperties": False,
            "required": ["immediate", "tactical", "structural"],
            "properties": {
                horizon: {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["label", "window", "summary", "fact_ids"],
                    "properties": {
                        "label": {"type": "string", "enum": AXIS_LABELS},
                        "window": {"type": "string", "const": window},
                        "summary": _TEXT_SCHEMA,
                        "confidence": {"type":"string","enum":CONFIDENCE_LABELS},
                        "coverage_limits": _TEXT_SCHEMA,
                        "fact_ids": _STRING_ARRAY_SCHEMA,
                    },
                }
                for horizon, window in (
                    ("immediate", "1—3个交易日"),
                    ("tactical", "1—4周"),
                    ("structural", "1—3个月"),
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

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.investment_contract import INVESTMENT_SCHEMA, validate_investment
from scripts.evidence import format_fact_evidence

ANALYSIS_JSON_SCHEMA["properties"]["investment_assessment"] = INVESTMENT_SCHEMA

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
_EXPLICIT_BAD_STATUSES = {
    "error",
    "failed",
    "missing",
    "not_available",
    "partial_latest",
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
    for key in ("source_status", "previous_source_status"):
        if fact.get(key) and fact[key] != "ok":
            return False
    for key in ("status", "freshness", "quality", "type"):
        status = fact.get(key)
        if isinstance(status, str) and (status.strip().lower().replace(" ", "_") in _EXPLICIT_BAD_STATUSES
                                       or "fetch_failure" in status.lower()):
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


def _validate_assessment_fact_ids(
    candidate: Mapping[str, Any], facts: Mapping[str, Mapping[str, Any]], errors: List[str]
) -> None:
    for section_name in ("axis_assessment", "horizon_assessment"):
        section = candidate.get(section_name)
        if not isinstance(section, dict):
            continue
        for item_name, item in section.items():
            if not isinstance(item, dict):
                continue
            fact_ids = item.get("fact_ids")
            if not isinstance(fact_ids, list):
                continue
            for index, fact_id in enumerate(fact_ids):
                if isinstance(fact_id, str) and fact_id not in facts:
                    errors.append(
                        f"$.{section_name}.{item_name}.fact_ids[{index}]: "
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
    r"(?P<number>[-+]?\d[\d,]*(?:\.\d+)?)\s*(?P<unit>%|bp|bps|bn|x|口|pt|mn/day)(?![A-Za-z0-9])",
    re.IGNORECASE,
)
_SLASH_DATE_PATTERN = re.compile(r"(?<!\d)\d{1,2}/\d{1,2}(?:[-~—至到]\d{1,2})?(?!\d)")


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


def materialize_evidence(candidate, model_input):
    facts, _ = _collect_facts(model_input)
    for _, claim in _iter_claims(candidate):
        if claim.get("evidence_refs"):
            claim["evidence"] = _render_claim_evidence(claim, facts)
    return candidate


def _render_claim_evidence(claim, facts):
    rendered = []
    for ref in claim["evidence_refs"]:
        fid = ref.get("fact_id") if isinstance(ref, dict) else None
        if not isinstance(fid, str) or fid not in facts or fid not in claim.get("fact_ids", []):
            raise ValueError("Evidence reference absent from claim facts: " + str(fid))
        rendered.append(format_fact_evidence(facts[fid]))
    return rendered

def _number_matches_fact(number: float, unit: str, fact_values: Sequence[float]) -> bool:
    candidates = [number]
    if unit == "%":
        candidates.append(number / 100.0)
    if unit in {"bp", "bps"}:
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
    text=_claim_text(claim)
    dates=set(re.findall(r"\b\d{4}-\d{2}-\d{2}\b",json.dumps(referenced,ensure_ascii=False)))
    for date in re.findall(r"\b\d{4}-\d{2}-\d{2}\b",text):
        if date not in dates:errors.append(f"{path}: date {date} not in referenced observations")
    for match in _UNIT_NUMBER_PATTERN.finditer(text):
        number=float(match.group('number').replace(',',''));unit=match.group('unit').lower()
        accepted=False
        for fact in referenced:
            native=str(fact.get('unit','')).lower();native={'bp avg':'bp'}.get(native,native)
            factor=100.0 if unit in ('bp','bps') and native=='%' else 1.0
            compatible=(unit==native or (unit=='bn' and native=='usd bn') or (unit=='mn/day' and native=='usd mn/day') or (unit in ('bp','bps') and native in ('%','bp','bps')) or (unit=='pt' and native in ('index','pt')) or (unit=='x' and native in ('ratio','x')) or (unit=='口' and not native))
            if not compatible:continue
            for field in ('value','previous','change','change_1d','change_5d','change_20d'):
                value=fact.get(field)
                if isinstance(value,(int,float)) and not isinstance(value,bool) and abs(number-value*factor)<=0.011:accepted=True
        if not accepted:errors.append(f"{path}: incompatible number/unit {match.group(0)!r}")


def _iter_narrative_text_fields(candidate: Mapping[str, Any]) -> Iterable[Tuple[str, str]]:
    """Yield (path, text) for prose strings that must obey the strict numeric-format rule.

    Excludes enum-like fields (priority/severity/type/label/confidence), fact_ids,
    related_indicators, dedupe_key and metric identifiers.
    """
    stance = candidate.get("stance")
    if isinstance(stance, dict):
        for key in ("score_text", "one_liner"):
            value = stance.get(key)
            if isinstance(value, str):
                yield f"$.stance.{key}", value
    axes = candidate.get("axis_assessment")
    if isinstance(axes, dict):
        for axis_name, axis in axes.items():
            if isinstance(axis, dict):
                summary = axis.get("summary")
                if isinstance(summary, str):
                    yield f"$.axis_assessment.{axis_name}.summary", summary
    horizons = candidate.get("horizon_assessment")
    if isinstance(horizons, dict):
        for horizon_name, horizon in horizons.items():
            if isinstance(horizon, dict):
                summary = horizon.get("summary")
                if isinstance(summary, str):
                    yield f"$.horizon_assessment.{horizon_name}.summary", summary
    for section in ("key_takeaways", "risk_flags"):
        items = candidate.get(section)
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            for key in ("title", "text", "condition"):
                value = item.get(key)
                if isinstance(value, str):
                    yield f"$.{section}[{index}].{key}", value
            evidence = item.get("evidence")
            if isinstance(evidence, list) and not item.get("evidence_refs"):
                for j, ev in enumerate(evidence):
                    if isinstance(ev, str):
                        yield f"$.{section}[{index}].evidence[{j}]", ev
    narratives = candidate.get("narrative_blocks")
    if isinstance(narratives, dict):
        for key in ("summary", "rates", "balance_sheet", "market_transmission"):
            value = narratives.get(key)
            if isinstance(value, str):
                yield f"$.narrative_blocks.{key}", value
        for module_key in ("treasury_yields", "jpy_carry"):
            module = narratives.get(module_key)
            if isinstance(module, dict):
                for key in ("one_liner", "analysis"):
                    value = module.get(key)
                    if isinstance(value, str):
                        yield f"$.narrative_blocks.{module_key}.{key}", value


def _number_has_indicator_context(text: str, start: int, end: int) -> bool:
    after = text[end:].lstrip()
    if after.startswith(("（", "(")):
        return True
    segment = text[:start]
    if re.search(r"[（(]\d{4}-\d{2}-\d{2}\s*[，,]\s*[^）)]*$", segment):
        return True
    return False


def _validate_narrative_numeric_format(candidate: Mapping[str, Any], errors: List[str]) -> None:
    """Enforce the strict numeric-format rule across all narrative prose fields.

    Rules:
    1. Any number carrying a market unit (%, bp, bps, bn, 口, pt, mn/day, x) must be
       written as 数量（更新时间，环比变化）, either as the level value immediately
       followed by the context paren or as the change value inside （date，change）.
    2. Dates must use full ISO (YYYY-MM-DD) and may not use slash shorthand (M/D or M/D-D).
    Exempt: bare counts/durations (e.g. 已滞后 N 日), priority labels (P0/P1/P2),
    metric identifiers and enum fields.
    """
    for path, text in _iter_narrative_text_fields(candidate):
        for match in _UNIT_NUMBER_PATTERN.finditer(text):
            if not _number_has_indicator_context(text, match.start(), match.end()):
                errors.append(
                    f"{path}: 提到带单位数值 {match.group(0)!r} 时必须使用 数量（更新时间，环比变化） 格式"
                )
                break
        if _SLASH_DATE_PATTERN.search(text):
            errors.append(f"{path}: 日期必须使用完整 ISO（YYYY-MM-DD），不得用 M/D 或 M/D-D 简写")


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
    content_keys = set()
    for path, claim in _iter_claims(candidate):
        content_key = json.dumps({k: claim.get(k) for k in ("text", "evidence", "fact_ids")}, ensure_ascii=False, sort_keys=True)
        if content_key in content_keys:
            errors.append(f"{path}: duplicate claim content")
        content_keys.add(content_key)
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

        if _UNIT_NUMBER_PATTERN.search(str(claim.get('text',''))):
            errors.append(f"{path}.text: market values belong in structured evidence_refs")
        if claim.get('evidence_refs'):
            try:
                expected = _render_claim_evidence(claim, facts)
                if claim.get('evidence') != expected:
                    errors.append(f"{path}.evidence: must match deterministic evidence_refs rendering")
            except (ValueError,KeyError,TypeError) as exc:
                errors.append(f"{path}.evidence_refs: {exc}")
        # Reference-backed evidence is checked verbatim above, including unit conversions.
        prose = {**claim, "evidence": []} if claim.get("evidence_refs") else claim
        _validate_claim_numbers(path, prose, facts, errors)

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
        or any(token in text for token in ("资金价格", "融资价格", "回购融资", "银行间融资", "回购市场", "隔夜融资", "资金市场", "融资失灵"))
    )


_P0_BENCHMARKS = {
    "metric:EFFR": ("metric:POLICY_UPPER_NYFED", "metric:DFEDTARU"),
    **{f"metric:{rate}": ("metric:SRP_RATE",) for rate in ("SOFR", "BGCR", "TGCR")},
}
_P0_CONFIRMATIONS = {
    "SRP_ACCEPTED": "facility", "REPO_FAILS_UST": "settlement",
    "BAMLH0A0HYM2": "credit", "BAMLC0A0CM": "credit", "VIXCLS": "volatility",
    "NFCI": "conditions", "SP500": "equities", "NASDAQCOM": "equities",
    "CBBTCUSD": "crypto", "UST_AUCTION_BTC": "auction", "TBILL_AUCTION_BTC": "auction",
}


def _p0_roots(fid, facts, ancestors=frozenset()):
    if fid in ancestors or fid not in facts:
        return set()
    deps = facts[fid].get("base_fact_ids") or []
    if not deps:
        return {fid}
    leaves = [_p0_roots(dep, facts, ancestors | {fid}) for dep in deps]
    return set.union(*leaves) if all(leaves) else set()


def _p0_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _p0_observation(fid, facts, cited, cutoff):
    """Return the market mechanism, interval, provenance and verified breach, if supported."""
    fact = facts[fid]
    end = fact.get("as_of")
    start = fact.get("window_start") or fact.get("previous_as_of")
    n = fact.get("window_observations", 1)
    if not isinstance(end, str) or not _parse_date(end) or (cutoff and end > cutoff):
        return None
    if cutoff:
        # The investment facts use these same observation-age rules for daily,
        # weekly and monthly series, including old captures with an "ok" flag.
        from scripts.investment_facts import _freshness
        if _freshness({**fact, "status": fact.get("status") or "ok"}, cutoff)[0] != "ok":
            return None
    if fact.get("window_end", end) != end or fact.get("previous_as_of", start) != start:
        return None
    if start and (not isinstance(start, str) or not _parse_date(start) or start >= end):
        return None
    roots = _p0_roots(fid, facts)
    value = fact.get("value")
    if not roots or not _p0_number(value):
        return None
    if fid in _P0_BENCHMARKS:
        for benchmark in _P0_BENCHMARKS[fid]:
            if benchmark not in cited:
                continue
            anchor = facts[benchmark]
            if (anchor.get("as_of") == end and anchor.get("unit") == fact.get("unit") == "%"
                    and _p0_number(anchor.get("value")) and value > anchor["value"]):
                return ("funding", start, end, n, roots | {benchmark}, True)
        return None
    if len(roots) != 1:
        return None
    leaf = next(iter(roots))
    parts = leaf.split(":")
    if len(parts) < 2 or parts[0] not in {"metric", "market"}:
        return None
    mechanism = _P0_CONFIRMATIONS.get(parts[1])
    if not mechanism:
        return None
    # Only these derived IDs repeat levels in their original units. Other
    # transformations, notably momentum scores, cannot be interpreted as levels.
    if fid.startswith("derived:") and fid not in {"derived:VIX_RISK", "derived:HY_CHANGE", "derived:IG_CHANGE", "derived:NFCI_LEVEL", "derived:AUCTION_BTC"}:
        return None
    previous = fact.get("previous")
    if mechanism == "auction" and fid.startswith("metric:") and fact.get("unit") in {"x", "ratio"} and 0 <= value < 1:
        return (mechanism, None, end, 1, roots, True)
    if not start or not _p0_number(previous):
        return None
    change = value - previous
    if mechanism in {"equities", "crypto", "auction"}:
        adverse = change < 0
    else:
        adverse = change > 0
    if not adverse or (mechanism in {"facility", "settlement"} and value <= 0):
        return None
    market_breach = False
    if leaf == fid == "market:SP500:level" and previous > 0:
        # NYSE Rule 7.12 uses the prior close. A capture with missing weekdays
        # cannot prove a one-session move. A closing move cannot prove a halt.
        prior, current = _parse_date(start), _parse_date(end)
        days = (current - prior).days
        adjacent = current.weekday() < 5 and days == (3 if current.weekday() == 0 else 1)
        market_breach = adjacent and value <= previous * 0.93
    return (mechanism, start, end, n, roots, market_breach)


def _p0_confirms(left, right, funding):
    mechanism, start, end, intervals, roots, breach = left
    other, other_start, other_end, other_intervals, other_roots, other_breach = right
    return (
        mechanism != other and roots.isdisjoint(other_roots)
        and end == other_end and intervals == other_intervals
        and (not start or not other_start or start == other_start)
        and (breach or other_breach)
        and (not funding or "funding" in {mechanism, other})
    )


def _validate_p0(
    candidate: Mapping[str, Any],
    facts: Mapping[str, Mapping[str, Any]],
    errors: List[str],
    cutoff: Optional[str] = None,
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
        if risk.get("claim_type") != "observed":
            errors.append(f"{path}: P0 只能陈述已经发生且有观测支持的压力")
        if risk.get("type") != "market":
            errors.append(f"{path}.type: P0 只能是已实现的 market 压力，不能是 data 风险")
        if risk.get("severity") != "high":
            errors.append(f"{path}.severity: P0 必须为 high")
        fact_ids = risk.get("fact_ids")
        if not isinstance(fact_ids, list):
            continue
        refs = risk.get("evidence_refs")
        cited = {ref.get("fact_id") for ref in (refs if isinstance(refs, list) else [])
                 if isinstance(ref, dict) and isinstance(ref.get("fact_id"), str)}
        cited.intersection_update(fid for fid in fact_ids if isinstance(fid, str) and fid in facts)
        stale = unfresh.intersection(fid for fid in fact_ids if isinstance(fid, str))
        if stale:
            errors.append(f"{path}.fact_ids: P0 引用了过期或抓取失败的数据 {sorted(stale)}")
        cited.difference_update(stale)
        observed = [_p0_observation(fid, facts, cited, cutoff) for fid in sorted(cited)]
        supported = [row for row in observed if row is not None]
        funding = _risk_is_funding_pressure(risk)
        if not any(_p0_confirms(a, b, funding) for i, a in enumerate(supported) for b in supported[i+1:]):
            errors.append(f"{path}.evidence_refs: P0 需要有依据的异常及同一观测窗口的独立压力佐证；融资异常须列同日核心利率与对应上限或常备回购报价")


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


_GAMMA = r"(?:gamma|伽马|伽玛|γ)"
_DEALER = r"(?:做市商|交易商|dealers?|market\s+makers?)"
_SIGN = r"(?:正|负|多头|空头|净多|净空|positive|negative|long|short)"
_OPTION_ASSERTION = re.compile(
    rf"{_GAMMA}\s*(?:挤压|轧空|逼空|squeeze)"
    rf"|{_DEALER}.{{0,25}}?(?:{_SIGN}\s*{_GAMMA}|{_GAMMA}\s*(?:敞口|暴露|头寸|仓位|方向|符号)?\s*"
    rf"(?:已(?:经)?|目前|当前|仍然|仍)?\s*(?:为|是|偏|呈|转为|转向|转|为净|is|are|has turned|turned)?\s*{_SIGN})"
    rf"|{_DEALER}.{{0,12}}?净\s*{_GAMMA}(?:的)?(?:方向|符号)?(?:已知|已经?确认|已明确|已经?翻转)"
    rf"|净\s*{_GAMMA}\s*(?:敞口|头寸|仓位|方向|符号)?(?:已(?:经)?|当前|仍)?(?:为|呈|偏|转为|转)[正负]"
    rf"|(?:市场|标普|SPX).{{0,8}}?(?:处于|转入|进入)\s*(?:净)?[正负]\s*{_GAMMA}"
    rf"|{_DEALER}.{{0,12}}?(?:被迫|追涨杀跌|对冲(?:盘|买盘|卖盘|买入|卖出)).{{0,10}}?(?:买入|卖出|买盘|卖盘|加仓|减仓|追涨|抛售|推动|推高|放大|压低|加速)"
    rf"|{_DEALER}.{{0,8}}?(?:已|正在|持续).{{0,8}}?(?:买入对冲|卖出对冲|追涨杀跌)"
    rf"|{_DEALER}.{{0,8}}?(?:被迫|被动)(?:追涨|杀跌|买入|卖出|买进|抛售)"
    rf"|{_DEALER}.{{0,8}}?(?:正在|已经?)(?:买入|卖出|抛售).{{0,8}}?对冲"
    rf"|(?:已突破|已触及|已确认|位于).{{0,8}}?(?:零\s*{_GAMMA}|gamma\s*flip)",
    re.IGNORECASE,
)
_SQUEEZE = re.compile(r"逼空|轧空|空头挤压|期权挤压|short\s+squeeze", re.I)
_US_EQUITY = re.compile(r"美股|美股期权|标普|纳指|纳斯达克|美国股指|股票期权|SPX|SPY|S&P\s*500|equity options", re.I)
_OTHER_MARKET = re.compile(r"日元|日股|日债|国债|美债|回购|人民币|比特币|加密|原油|JPY|JGB|Treasur(?:y|ies)|Bitcoin", re.I)
_OPTION_QUALIFIER = re.compile(
    r"能否|是否|未知|不明|不清楚|无法|不能(?:确认|推断|证明|判断|判定|断言|认定)|尚无|无从|尚待|有待|未(?:见|获|能|得到|确认|证实|知|发生|出现|形成)"
    r"|缺少|缺乏|不足以|没有证据|未经证实|难以确认|不代表|不意味着|不等于|未必|不能据此|需要.*(?:证据|验证)"
    r"|若|如果|假如|假设|一旦|有可能|可能|才(?:能|会|可)|取决于|情景|警惕|防范|留意|观察是否"
    r"|\b(?:if|unless|could|might|hypothetical|unconfirmed|unknown|cannot|whether|no evidence)\b",
    re.IGNORECASE,
)
_REALIZED = re.compile(r"已经?|正在|当前|目前|证实|确认|确定|现实中|\b(?:underway|already|now|confirmed)\b", re.I)
_CHAIN_OBSERVATION = re.compile(
    rf"(?:无符号|全市场|市场总|持仓总|总)\s*{_GAMMA}(?:敞口|规模|暴露|水平)?"
    rf"|(?:到期|0DTE).{{0,8}}?{_GAMMA}\s*占比", re.I,
)
_CHAIN_LEVEL = re.compile(r"为正|为零|上升|升高|下滑|下降|扩大|收窄|集中|高位|低位|增加|减少|偏高|偏低|飙升|升至|降至|持平")


def _option_texts(value, path="$", refs=None, scenario=False):
    if isinstance(value, dict):
        if isinstance(value.get("fact_ids"), list):
            refs = {fid for fid in value["fact_ids"] if isinstance(fid, str)}
        scenario = scenario or value.get("claim_type") == "scenario"
        for key, item in value.items():
            if key not in {"fact_ids", "change_fact_ids", "related_indicators", "dedupe_key", "evidence", "evidence_refs"}:
                yield from _option_texts(item, f"{path}.{key}", refs, scenario or key == "scenarios")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from _option_texts(item, f"{path}[{i}]", refs, scenario)
    elif isinstance(value, str):
        yield path, value, refs, scenario


def _validate_option_claims(candidate, package, facts, errors):
    # Old packages retain the contract used to generate them. In the current
    # contract even a complete unsigned chain contains no signed dealer inventory.
    if package.get("research_version") not in {"3.2", "3.3"} and not any(fid.startswith("option:") for fid in facts):
        return
    for path, text, refs, scenario in _option_texts(candidate):
        for sentence in re.split(r"[。；;！!\n]|(?:但是|但(?!凡)|然而|不过|其实|实际上|\bbut\b)", text, flags=re.I):
            hypothesized = False
            clauses = re.split(r"[，,]", sentence)
            for clause in clauses:
                clause = clause.strip()
                if not clause:
                    continue
                condition = re.match(r"^(?:若|如果|假如|假设|一旦|仅当|只有|if\b)", clause, re.I)
                # A condition may govern the following clause. An explicit
                # observation in that clause still needs direct evidence.
                hypothetical = bool(condition) or (hypothesized and not _REALIZED.search(clause))
                hypothesized = hypothesized or bool(condition)
                if hypothetical or clause.endswith(("？", "?")):
                    continue
                assertion = _OPTION_ASSERTION.search(clause)
                # Other markets can experience short squeezes independently of
                # equity-option gamma. Match a bare squeeze only in its market.
                squeeze = _SQUEEZE.search(clause) if not assertion else None
                if squeeze:
                    subject = clause[:squeeze.start()]
                    equities = list(_US_EQUITY.finditer(subject))
                    others = list(_OTHER_MARKET.finditer(subject))
                    if equities or others:
                        in_equities = bool(equities and (not others or equities[-1].start() > others[-1].start()))
                    else:
                        in_equities = not _OTHER_MARKET.search(clause) and (
                            _US_EQUITY.search(sentence) or re.search(_GAMMA, sentence, re.I)
                            or path.startswith("$.investment_assessment.equities.")
                            or (refs and any(fid.startswith("option:") for fid in refs)))
                    if in_equities:
                        assertion = squeeze
                chain = _CHAIN_OBSERVATION.search(clause)
                mention = assertion or chain
                if not mention:
                    continue
                # A hedge such as "可能放大波动" after a definitive inventory
                # statement does not make that inventory statement conditional.
                tail = clause[mention.end():].strip()
                qualifier = re.match(r"(?:的(?:方向|风险|证据|符号|存在))?(?:目前|仍然|并|尚|仍|暂时|还)?(.*)", tail)
                if (_OPTION_QUALIFIER.search(clause[:mention.end()])
                        or _OPTION_QUALIFIER.match(qualifier.group(1)) or tail.startswith("还是")):
                    continue
                if assertion:
                    if not _REALIZED.search(clause) and (
                        "风险" in clause or "的条件" in clause or "的证据" in clause
                        or (scenario and path.endswith((".title", ".trigger", ".condition", ".invalidation")))
                    ):
                        continue
                    errors.append(f"{path}: 当前期权事实无法确认做市商净Gamma、实际对冲流或已经发生的挤压。请陈述可核验观测，或说明情景触发条件。")
                    break
                if chain and _CHAIN_LEVEL.search(clause):
                    key = "gross_gamma_1pct"
                    if "占比" in clause:
                        key = "gamma_share_0dte" if re.search("当日|当天|0dte", clause, re.I) else "gamma_share_7d"
                    fid = "option:SPX:" + key
                    fact = facts.get(fid, {})
                    if (fact.get("status") != "ok" or fact.get("value") is None
                            or (refs is not None and fid not in refs)):
                        errors.append(f"{path}: 报告已观测的持仓Gamma或到期占比须有对应的有效逐合约事实 {fid}。")
                        break


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
    _validate_assessment_fact_ids(candidate, facts, errors)
    _validate_claims(candidate, facts, errors)
    _validate_narrative_numeric_format(candidate, errors)
    generated_day = str(model_input.get("generated_at_bjt") or "")[:10]
    report_day = (candidate.get("meta") or {}).get("data_as_of") if isinstance(candidate.get("meta"), dict) else None
    cutoffs = [day for day in (generated_day, report_day) if isinstance(day, str) and _parse_date(day)]
    _validate_p0(candidate, facts, errors, min(cutoffs) if cutoffs else None)
    _validate_required_modules(candidate, model_input, errors)
    _validate_uncited_predictions(candidate, errors)
    _validate_option_claims(candidate, model_input, facts, errors)
    errors.extend(validate_investment(candidate, model_input, facts, _unfresh_fact_ids(facts)))
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
    # Mark the published artifact so the frontend can read it inline from data.js
    # (no HTTP fetch needed) and distinguish it from run.py's pending placeholder.
    candidate.setdefault("meta", {})["status"] = "published"
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
