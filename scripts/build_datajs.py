#!/usr/bin/env python3
"""Bake output/latest/{dashboard_data.json, analysis.json} into frontend/usd-liquidity-monitor/data.js.

Why this exists:
- run.py generates data.js at the very start of the pipeline, when analysis.json is still a
  `pending_model_analysis` placeholder. So the baked window.ANALYSIS_DATA is a placeholder, and the
  frontend falls back to fetch('/output/latest/analysis.json') — which only works under an HTTP server.
- This script is the FINAL step of the pipeline: after the model publishes the real analysis.json,
  it re-bakes data.js so window.ANALYSIS_DATA carries the published analysis. The frontend then reads
  the global directly (no fetch, no server) and the page works opened as a file:// URL.

Usage:
    python3 scripts/build_datajs.py [--require-published] [--latest-dir DIR] [--frontend-dir DIR]
"""
import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LATEST = PROJECT_ROOT / "output" / "latest"
DEFAULT_FRONTEND = PROJECT_ROOT / "frontend" / "usd-liquidity-monitor"


def main() -> int:
    parser = argparse.ArgumentParser(description="Bake latest dashboard+analysis into data.js")
    parser.add_argument("--latest-dir", default=str(DEFAULT_LATEST), help="Directory containing dashboard_data.json and analysis.json")
    parser.add_argument("--frontend-dir", default=str(DEFAULT_FRONTEND), help="Frontend directory that holds data.js")
    parser.add_argument(
        "--require-published",
        action="store_true",
        help="Exit non-zero if analysis.json status is not 'published' (fail the pipeline instead of baking a placeholder)",
    )
    args = parser.parse_args()

    latest_dir = Path(args.latest_dir)
    frontend_dir = Path(args.frontend_dir)
    dashboard_path = latest_dir / "dashboard_data.json"
    analysis_path = latest_dir / "analysis.json"

    if not dashboard_path.exists():
        print(f"[build_datajs] MISSING dashboard_data.json: {dashboard_path}", file=sys.stderr)
        return 2
    if not analysis_path.exists():
        print(f"[build_datajs] MISSING analysis.json: {analysis_path}", file=sys.stderr)
        return 2

    dashboard_data = json.loads(dashboard_path.read_text(encoding="utf-8"))
    analysis_data = json.loads(analysis_path.read_text(encoding="utf-8"))

    status = (analysis_data.get("meta") or {}).get("status", "unknown")
    if status == "pending_model_analysis":
        print(f"[build_datajs] WARNING: analysis.json status is '{status}' (placeholder). "
              f"The file:// page will show '待模型分析'.", file=sys.stderr)
        if args.require_published:
            print("[build_datajs] --require-published set: refusing to bake placeholder.", file=sys.stderr)
            return 3
    elif status != "published":
        print(f"[build_datajs] NOTE: analysis.json status is '{status}' (expected 'published').", file=sys.stderr)
    else:
        print(f"[build_datajs] analysis.json status OK: published")

    data_js = (
        f"window.DASHBOARD_DATA = {json.dumps(dashboard_data, ensure_ascii=False, indent=2)};\n"
        f"window.ANALYSIS_DATA = {json.dumps(analysis_data, ensure_ascii=False, indent=2)};\n"
    )
    out_path = frontend_dir / "data.js"
    out_path.write_text(data_js, encoding="utf-8")
    print(f"[build_datajs] wrote {out_path} ({len(data_js)} bytes) — dashboard + analysis baked inline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
