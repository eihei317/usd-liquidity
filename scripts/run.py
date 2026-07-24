#!/usr/bin/env python3
"""Main entry point for USD Liquidity Monitor — orchestrates fetch, signals, charts, output."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure parent dir is on path for relative imports when run as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils import (
    DerivedSignal,
    LATEST_DIR,
    Metric,
    OUTPUT_DIR,
    ROOT,
    now_bjt,
    load_jpy_carry_history_payload,
)
from scripts.fetchers import fetch_all_metrics, fetch_upcoming_auctions
from scripts.signals import derive_signals, stance_from_score
from scripts.charts import fetch_chart_series, write_liquidity_charts
from scripts.dashboard import augment_charts_payload, build_charts_payload, build_dashboard_data
from scripts.analysis import build_report
from scripts.db import init_db, ingest_snapshot


def refresh_jpy_carry_history(trigger: str) -> Optional[Dict[str, Any]]:
    """Run the JPY carry history script and return the payload."""
    import subprocess
    script = ROOT / "scripts" / "jpy_carry.py"
    if not script.exists():
        # Fall back to original name
        script = ROOT / "scripts" / "jpy_carry_history.py"
    if not script.exists():
        return load_jpy_carry_history_payload()
    try:
        subprocess.run(
            [sys.executable or "/usr/bin/python3", str(script), trigger or "更新日元carry数据", "--json"],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except Exception:
        pass
    return load_jpy_carry_history_payload()


def write_outputs(
    report: str,
    context: Dict[str, Any],
    model_input: Dict[str, Any],
    dashboard_data: Dict[str, Any],
    charts_payload: Dict[str, Any],
    stamp: str,
) -> Dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "report_path": OUTPUT_DIR / f"usd_liquidity_brief_{stamp}.md",
        "json_path": OUTPUT_DIR / f"usd_liquidity_snapshot_{stamp}.json",
        "model_input_path": OUTPUT_DIR / f"usd_liquidity_model_input_{stamp}.json",
        "dashboard_data_path": OUTPUT_DIR / f"usd_liquidity_dashboard_data_{stamp}.json",
        "charts_json_path": OUTPUT_DIR / f"usd_liquidity_charts_{stamp}.json",
    }
    paths["report_path"].write_text(report, encoding="utf-8")
    paths["json_path"].write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["model_input_path"].write_text(json.dumps(model_input, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["dashboard_data_path"].write_text(json.dumps(dashboard_data, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["charts_json_path"].write_text(json.dumps(charts_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    latest_map = {
        "snapshot.json": context,
        "model_input.json": model_input,
        "dashboard_data.json": dashboard_data,
        "charts.json": charts_payload,
    }
    # Always reset analysis to a placeholder after fresh data generation.
    # The model/agent must read the newly generated model_input.json and overwrite this file;
    # preserving an older analysis here would risk showing stale conclusions with fresh data.
    latest_map["analysis.json"] = {
        "meta": {"status": "pending_model_analysis", "generated_at_bjt": context.get("generated_at_bjt", "")},
        "stance": {"label": "待模型分析", "score_text": "", "one_liner": ""},
        "key_takeaways": [],
        "risk_flags": [],
        "narrative_blocks": {}
    }
    # analysis.json is intentionally a latest-only model artifact. A timestamped copy written
    # here would remain as a pending placeholder after the model publishes the validated result,
    # making the CLI-reported analysis path misleading.
    paths["analysis_path"] = LATEST_DIR / "analysis.json"

    for filename, payload in latest_map.items():
        (LATEST_DIR / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Generate data.js for inline data (avoids fetch/CORS issues in preview panel)
    frontend_dir = ROOT / "frontend" / "usd-liquidity-monitor"
    if frontend_dir.exists():
        analysis_for_frontend = latest_map.get("analysis.json", {
            "meta": {"status": "pending_model_analysis"},
            "stance": {"label": "待模型分析", "score_text": "", "one_liner": ""},
            "key_takeaways": [],
            "risk_flags": [],
            "narrative_blocks": {}
        })
        data_js = f"window.DASHBOARD_DATA = {json.dumps(dashboard_data, ensure_ascii=False, indent=2)};\nwindow.ANALYSIS_DATA = {json.dumps(analysis_for_frontend, ensure_ascii=False, indent=2)};\n"
        (frontend_dir / "data.js").write_text(data_js, encoding="utf-8")

    return paths


def cleanup_old_outputs(current_stamp: str) -> int:
    patterns = [
        "usd_liquidity_brief_*.md",
        "usd_liquidity_snapshot_*.json",
        "usd_liquidity_model_input_*.json",
        "usd_liquidity_dashboard_data_*.json",
        "usd_liquidity_analysis_*.json",
        "usd_liquidity_charts_*.json",
        "usd_liquidity_chart_*.svg",
    ]
    removed = 0
    for pattern in patterns:
        for path in OUTPUT_DIR.glob(pattern):
            if current_stamp in path.name:
                continue
            if path.is_file():
                path.unlink()
                removed += 1
    return removed


def load_snapshot(path: Path) -> Tuple[List[Metric], List[DerivedSignal], float, List[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    metrics = [Metric(**item) for item in payload.get("metrics", [])]
    # A reused snapshot is a raw-data replay, not a replay of old analysis logic. Always rebuild
    # derived signals so prompt/signal fixes are exercised and stale serialized conclusions cannot
    # silently survive a code update.
    signals, score, highlights = derive_signals(metrics)
    return metrics, signals, score, highlights


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch USD liquidity data and generate a daily briefing")
    parser.add_argument("trigger", nargs="*", help="Natural-language trigger, e.g. 今天美元流动性如何")
    parser.add_argument("--auction-lookback-days", type=int, default=21, help="Lookback window for Treasury auctions")
    parser.add_argument("--input-json", help="Reuse an existing usd_liquidity_snapshot_*.json instead of fetching live data")
    parser.add_argument("--model-input-only", action="store_true", help="Still writes all files, but console output focuses on model_input_path")
    parser.add_argument("--no-charts", action="store_true", help="Skip SVG chart generation")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output paths as JSON")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    trigger = " ".join(args.trigger).strip()

    # Ensure DB exists
    init_db()

    if args.input_json:
        metrics, signals, score, highlights = load_snapshot(Path(args.input_json))
    else:
        metrics = fetch_all_metrics(args.auction_lookback_days)
        signals, score, highlights = derive_signals(metrics)

    upcoming_auctions = fetch_upcoming_auctions(60)

    stamp = now_bjt().strftime("%Y%m%d_%H%M%S")
    chart_paths: List[str] = []
    series_bundle: Dict[str, List[Tuple[str, float]]] = {}

    # 先生成基础 snapshot 并落库。前端图表必须在本次 snapshot 落库后，
    # 再从 SQLite 读取，避免图表层重复调用 API 或读取旧数据。
    refresh_jpy_carry_history(trigger or "更新日元carry数据")
    report, context, model_input = build_report(trigger, metrics, signals, score, highlights, chart_paths, upcoming_auctions)
    snapshot_path = OUTPUT_DIR / f"usd_liquidity_snapshot_{stamp}.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        ingest_snapshot(str(snapshot_path))
        print(f"[DB] 历史库已更新：{snapshot_path.name}")
    except Exception as db_exc:
        print(f"[DB] 落库失败：{db_exc}")

    if not args.no_charts:
        try:
            series_bundle = fetch_chart_series(45)
            chart_paths = [str(path) for path in write_liquidity_charts(stamp, series_bundle)]
            # chart_paths 变更后重建 context/model_input，使输出产物自洽。
            report, context, model_input = build_report(trigger, metrics, signals, score, highlights, chart_paths, upcoming_auctions)
        except Exception as exc:
            highlights.append(f"图表生成失败：{exc}")
            report, context, model_input = build_report(trigger, metrics, signals, score, highlights, chart_paths, upcoming_auctions)

    charts_payload = augment_charts_payload(build_charts_payload(series_bundle, upcoming_auctions), upcoming_auctions)
    generated = context["generated_at_bjt"]
    dashboard_data = build_dashboard_data(trigger, generated, context, metrics, signals, charts_payload, chart_paths, upcoming_auctions)
    output_paths = write_outputs(report, context, model_input, dashboard_data, charts_payload, stamp)

    cleanup_removed = cleanup_old_outputs(stamp)

    if args.json:
        print(json.dumps({**{key: str(value) for key, value in output_paths.items()}, "latest_dir": str(LATEST_DIR), "chart_paths": chart_paths, "cleanup_removed": cleanup_removed, "stance": context["stance"], "score": context["score"]}, ensure_ascii=False))
    else:
        print(f"美元流动性总判断：{context['stance']} | 分数：{context['score']:.1f}")
        print(f"Markdown简报：{output_paths['report_path']}")
        print(f"JSON快照：{output_paths['json_path']}")
        print(f"模型输入包：{output_paths['model_input_path']}")
        print(f"前端数据：{output_paths['dashboard_data_path']}")
        print(f"分析结果：{output_paths['analysis_path']}")
        print(f"最新数据目录：{LATEST_DIR}")
        print(f"清理旧产物：{cleanup_removed} 个")
        for chart_path in chart_paths:
            print(f"图表：{chart_path}")
        if args.model_input_only:
            print("提示：模型输入包已生成，可交给模型连同分析prompt进行最终分析。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
