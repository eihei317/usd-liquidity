"""Prospective, immutable research observations; never a trading backtest.

This module performs no network requests and writes no files. A coordinator stores
one research_record.json inside each atomically published run. Price dates have no
intraday timestamps, so the observation rule deliberately leaves two UTC dates
on each side of the publication/evaluation boundary.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

BJT = timezone(timedelta(hours=8))
METHOD_VERSION = "3.0"
ASSETS = {
    "equities": {"name": "美股", "series": "SP500", "windows": (10, 20, 60), "calendar": False},
    "bitcoin": {"name": "BTC", "series": "CBBTCUSD", "windows": (14, 28, 84), "calendar": True},
}
METHODOLOGY_NOTE = (
    "这是判断发布后的价格观察记录，不是交易策略收益或实际成交记录。"
    "原始日价缺少精确发布时间，采用保守规则：实际发布时间转为UTC后，"
    "从其日期往后两日开始寻找首个有效收盘作为观察起点；"
    "评估只使用截至评估时刻UTC日期往前两日的价格。"
    "美股按10／20／60个后续有效收盘观察（约2／4／12周），"
    "BTC按14／28／84个自然日观察，缺少窗口内日价则保持缺失。"
    "同一快照与方法版本仅首次发布算一个样本。"
    "去重后的持有窗口仍可能重叠，不能当作统计独立样本；"
    "历史价格截断或起点缺价时不把观察起点向后漂移。"
    "收益基线是同一资产、同一窗口的持有价格变化，未扣费用且不含股息，"
    "不能用它宣称择时超额收益。流动性支持或压制也不等于买卖指令。"
    "所有已成熟样本均保留；分组不足十个样本时明确标为积累中，"
    "样本充足时仍只提供描述统计，预测能力需要另行样本外检验。"
)


def _timestamp(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        result = value
    elif isinstance(value, str):
        normalized = value.strip().replace(" UTC", "").replace("Z", "+00:00")
        try:
            result = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise ValueError("研究记录时间必须为有效ISO时间或北京时间字符串") from exc
    else:
        raise ValueError("研究记录时间缺失")
    # The named API accepts Beijing timestamps; legacy generated_at lacks tzinfo.
    return result.replace(tzinfo=BJT) if result.tzinfo is None else result


def _version(model_input: dict) -> str:
    return str(model_input.get("research_version") or METHOD_VERSION)


def create_research_record(run_id, analysis, model_input, published_at_bjt, input_sha256) -> dict:
    """Freeze a complete investment assessment at its actual publication time."""
    if not isinstance(run_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
        raise ValueError("Invalid research run_id")
    assessment = analysis.get("investment_assessment")
    if not isinstance(assessment, dict) or any(not isinstance(assessment.get(a), dict) for a in ASSETS):
        raise ValueError("投资研究结论不完整，不能生成留档")
    generated = model_input.get("generated_at_bjt")
    source_time = _timestamp(generated)
    publication = _timestamp(published_at_bjt)
    if publication < source_time:
        raise ValueError("实际发布时间不得早于事实包生成时间")
    digest = str(input_sha256)
    if not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
        raise ValueError("研究记录必须包含有效的输入SHA256")
    version = _version(model_input)
    source_stamp = source_time.astimezone(BJT).isoformat()
    dedupe = hashlib.sha256(json.dumps(
        {"source_generated_at_bjt": source_stamp, "method_version": version},
        sort_keys=True, ensure_ascii=False,
    ).encode("utf-8")).hexdigest()
    return {
        "schema_version": METHOD_VERSION,
        "run_id": run_id,
        "method_version": version,
        "model": analysis.get("meta", {}).get("model", "unknown"),
        "source_generated_at_bjt": source_stamp,
        "source_data_as_of": analysis.get("meta", {}).get("data_as_of"),
        "published_at_bjt": publication.astimezone(BJT).isoformat(),
        "input_sha256": digest.lower(),
        "dedupe_key": dedupe,
        "historical_snapshot": source_time.astimezone(BJT).date() < publication.astimezone(BJT).date(),
        "assessment": copy.deepcopy(assessment),
        "entry_rule": "first valid price date >= UTC publication date + 2 calendar days",
        "evaluation_cutoff_rule": "price date <= UTC evaluation date - 2 calendar days",
        "record_type": "prospective_research_observation",
    }


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_published_records(output_dir: Path) -> list:
    """Read only the published lineage, verifying archived record hashes.

    Failed or merely prepared runs are never scanned. New manifests and records
    retain previous_run_id. A legacy run with neither field ends the lineage.
    """
    root = Path(output_dir).resolve()
    pointer_path = root / "current.json"
    if not pointer_path.exists():
        return []
    pointer = _json(pointer_path)
    run_id = pointer.get("run_id")
    if pointer.get("directory") != "runs/" + str(run_id):
        raise ValueError("当前发布指针目录与run_id不匹配")
    records, visited = [], set()
    first = True
    while run_id:
        if not isinstance(run_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
            raise ValueError("研究历史含非法运行标识")
        if run_id in visited:
            raise ValueError("研究发布历史存在循环")
        visited.add(run_id)
        directory = root / "runs" / run_id
        manifest_path = directory / "manifest.json"
        if not manifest_path.is_file():
            raise ValueError("已发布研究运行缺少manifest: " + run_id)
        manifest_bytes = manifest_path.read_bytes()
        if first and pointer.get("manifest_sha256"):
            if hashlib.sha256(manifest_bytes).hexdigest() != pointer["manifest_sha256"]:
                raise ValueError("当前研究manifest哈希不匹配")
        manifest = json.loads(manifest_bytes.decode("utf-8-sig"))
        if manifest.get("run_id") != run_id:
            raise ValueError("研究manifest运行标识不匹配")
        record_path = directory / "research_record.json"
        record = None
        if record_path.exists():
            expected = manifest.get("files", {}).get("research_record.json")
            record_bytes = record_path.read_bytes()
            if not expected or hashlib.sha256(record_bytes).hexdigest() != expected:
                raise ValueError("已发布研究记录哈希不匹配: " + run_id)
            record = json.loads(record_bytes.decode("utf-8-sig"))
            if record.get("run_id") != run_id:
                raise ValueError("研究记录运行标识不匹配")
            records.append(record)
        if record and "previous_run_id" in record:
            next_id = record["previous_run_id"]
        elif "previous_run_id" in manifest:
            next_id = manifest["previous_run_id"]
        else:
            # The pointer's previous_run_id is rollback navigation, not lineage.
            # In particular, rolling back from new A to legacy B makes it point
            # forward to A. Following it here would create B -> A -> B cycles.
            next_id = None
        run_id, first = next_id, False
    return sorted(records, key=lambda r: (_timestamp(r["published_at_bjt"]), r["run_id"]))


def _prices(rows, cutoff: date) -> tuple[list[tuple[date, float]], dict]:
    by_date, conflicts = {}, set()
    quality = {"invalid_rows": 0, "future_rows_excluded": 0, "conflicting_dates": []}
    for row in rows if isinstance(rows, list) else []:
        try:
            if not isinstance(row, dict):
                raise ValueError("bad row")
            day_text, value = row.get("date"), row.get("value")
            day = date.fromisoformat(day_text)
            if day.isoformat() != day_text or isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("bad type")
            value = float(value)
            if not math.isfinite(value) or value <= 0:
                raise ValueError("bad price")
        except (ValueError, TypeError, OverflowError):
            quality["invalid_rows"] += 1
            continue
        if day > cutoff:
            quality["future_rows_excluded"] += 1
            continue
        if day in by_date and by_date[day] != value:
            conflicts.add(day)
        by_date[day] = value
    for day in conflicts:
        by_date.pop(day, None)
    quality["conflicting_dates"] = sorted(d.isoformat() for d in conflicts)
    return sorted(by_date.items()), quality


def _row_base(record: dict, asset: str, window: int, cutoff: date) -> dict:
    config = ASSETS[asset]
    label = f"{window}个自然日" if config["calendar"] else f"{window}个有效交易观测"
    decision = record.get("assessment", {}).get(asset, {})
    return {
        "run_id": record["run_id"],
        "published_at_bjt": record["published_at_bjt"],
        "source_generated_at_bjt": record.get("source_generated_at_bjt"),
        "method_version": record.get("method_version"),
        "asset": asset,
        "asset_name": config["name"],
        "price_series": config["series"],
        "horizon": label,
        "window": window,
        "window_basis": "calendar_days" if config["calendar"] else "valid_trading_observations",
        "liquidity_bias": decision.get("liquidity_bias", "数据不足"),
        "confidence": decision.get("confidence"),
        "status": "pending",
        "status_note": "等待发布后的观察价格和完整持有窗口。",
        "evaluation_price_cutoff": cutoff.isoformat(),
        "entry_date": None,
        "entry_price": None,
        "exit_date": None,
        "exit_price": None,
        "elapsed_calendar_days": None,
        "return_pct": None,
        "max_drawdown_pct": None,
        "max_adverse_excursion_pct": None,
        "benchmark_return_pct": None,
    }


def _evaluate(record: dict, asset: str, window: int, rows, cutoff: date) -> dict:
    result = _row_base(record, asset, window, cutoff)
    minimum_entry = _timestamp(record["published_at_bjt"]).astimezone(timezone.utc).date() + timedelta(days=2)
    result["minimum_entry_date"] = minimum_entry.isoformat()
    if minimum_entry > cutoff:
        return result
    eligible = [(d, p) for d, p in rows if d >= minimum_entry]
    if not eligible:
        result.update(status="missing_price", status_note="观察起点已到，价格源没有发布后的有效价格。")
        return result
    config = ASSETS[asset]
    entry_day, entry_price = eligible[0]
    if config["calendar"] and entry_day != minimum_entry:
        result.update(status="missing_price", status_note="BTC观察起点自然日缺价，不能向后移动起点。")
        return result
    if not config["calendar"] and entry_day != minimum_entry:
        prior = [d for d, _ in rows if d < minimum_entry]
        if not prior or (entry_day - prior[-1]).days > 7:
            result.update(status="missing_price", status_note="美股起点附近的历史缺失或截断，不能确认首个有效收盘。")
            return result
    result.update(entry_date=entry_day.isoformat(), entry_price=entry_price)
    if config["calendar"]:
        exit_day = entry_day + timedelta(days=window)
        result["target_exit_date"] = exit_day.isoformat()
        if exit_day > cutoff:
            return result
        by_date = dict(eligible)
        path_days = [entry_day + timedelta(days=i) for i in range(window + 1)]
        missing = [d.isoformat() for d in path_days if d not in by_date]
        if missing:
            result.update(status="missing_price", missing_dates=missing,
                          status_note="BTC自然日窗口缺少日价，保持收益及完整回撤未知。")
            return result
        path = [(d, by_date[d]) for d in path_days]
    else:
        if len(eligible) <= window:
            result["observations_available"] = max(0, len(eligible) - 1)
            return result
        path = eligible[:window + 1]
    exit_day, exit_price = path[-1]
    change = (exit_price / entry_price - 1) * 100
    peak, drawdown = entry_price, 0.0
    for _, value in path:
        peak = max(peak, value)
        drawdown = min(drawdown, (value / peak - 1) * 100)
    adverse = min(0.0, (min(v for _, v in path) / entry_price - 1) * 100)
    result.update(
        status="available", status_note="窗口已成熟；数值为观察期价格表现，不是策略收益。",
        exit_date=exit_day.isoformat(), exit_price=exit_price,
        elapsed_calendar_days=(exit_day - entry_day).days,
        return_pct=round(change, 4), benchmark_return_pct=round(change, 4),
        max_drawdown_pct=round(drawdown, 4), max_adverse_excursion_pct=round(adverse, 4),
    )
    return result


def build_research_review(records: list, price_history: dict, as_of_bjt: str) -> dict:
    """Observe all published assessments without inventing a buy/sell strategy."""
    as_of = _timestamp(as_of_bjt)
    cutoff = as_of.astimezone(timezone.utc).date() - timedelta(days=2)
    accepted, excluded = [], []
    for record in records if isinstance(records, list) else []:
        try:
            if not isinstance(record, dict) or not record.get("dedupe_key") or not record.get("run_id"):
                raise ValueError("研究记录缺少唯一标识")
            pub = _timestamp(record.get("published_at_bjt"))
            source = _timestamp(record.get("source_generated_at_bjt"))
            if pub < source:
                raise ValueError("发布时间早于事实包")
            if pub > as_of:
                raise ValueError("记录在本次评估时点尚未发布")
            if not isinstance(record.get("assessment"), dict):
                raise ValueError("缺少冻结的投资结论")
            accepted.append(record)
        except (ValueError, TypeError, KeyError) as exc:
            excluded.append({"run_id": record.get("run_id") if isinstance(record, dict) else None,
                             "reason": str(exc)})
    accepted.sort(key=lambda r: (_timestamp(r["published_at_bjt"]), r["run_id"]))
    independent, seen, duplicates = [], set(), []
    for record in accepted:
        key = record["dedupe_key"]
        if key in seen:
            duplicates.append(record["run_id"])
        else:
            seen.add(key)
            independent.append(record)
    history = price_history if isinstance(price_history, dict) else {}
    prices, quality = {}, {}
    for asset, config in ASSETS.items():
        prices[asset], quality[config["series"]] = _prices(history.get(config["series"], []), cutoff)
    observations = [
        _evaluate(record, asset, window, prices[asset], cutoff)
        for record in independent for asset, config in ASSETS.items() for window in config["windows"]
    ]
    grouped = defaultdict(list)
    for row in observations:
        grouped[(row["method_version"], row["asset"], row["horizon"], row["liquidity_bias"])].append(row)
    groups = []
    for (method, asset, horizon, bias), items in sorted(grouped.items(), key=lambda item: tuple(str(x) for x in item[0])):
        mature = [r for r in items if r["status"] == "available"]
        mean = lambda name: round(sum(r[name] for r in mature) / len(mature), 4) if mature else None
        groups.append({
            "method_version": method, "asset": asset, "asset_name": ASSETS[asset]["name"],
            "horizon": horizon, "liquidity_bias": bias, "n": len(mature),
            "pending_n": sum(r["status"] == "pending" for r in items),
            "missing_price_n": sum(r["status"] == "missing_price" for r in items),
            "mean_return_pct": mean("return_pct"),
            "mean_max_drawdown_pct": mean("max_drawdown_pct"),
            "mean_max_adverse_excursion_pct": mean("max_adverse_excursion_pct"),
            "conclusion_status": "样本不足，持续积累" if len(mature) < 10 else "仅描述统计，尚需样本外验证",
        })
    mature_count = sum(r["status"] == "available" for r in observations)
    return {
        "schema_version": METHOD_VERSION,
        "status": "available" if mature_count else "collecting",
        "as_of_bjt": as_of.astimezone(BJT).isoformat(),
        "evaluation_price_cutoff": cutoff.isoformat(),
        "methodology_note": METHODOLOGY_NOTE,
        "independent_record_count": len(independent),
        "mature_observation_count": mature_count,
        "excluded_duplicate_run_ids": duplicates,
        "excluded_records": excluded,
        "price_quality": quality,
        "records": observations,
        "groups": groups,
    }
