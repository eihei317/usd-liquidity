#!/usr/bin/env python3
"""Call Tencent TokenHub HY3 for USD-liquidity analysis and publish validated JSON.

This adapter is optional: data fetching remains independent from model analysis. It sends the
already-built model_input.json, requests a function/tool response, validates the candidate, and
atomically publishes analysis.json only when validation succeeds.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analysis_validator import build_hy3_tool_definition, publish_analysis_candidate

DEFAULT_ENDPOINT = "https://tokenhub.tencentmaas.com/v1/chat/completions"
DEFAULT_MODEL = "hy3"


def _compact_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def build_request_payload(model_input: Dict[str, Any], model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """Build an OpenAI-compatible HY3 request using a function schema for the final answer."""
    prompt = model_input.get("analysis_prompt") or ""
    facts = {key: value for key, value in model_input.items() if key != "analysis_prompt"}
    return {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": "以下是本次唯一可用的结构化事实包。请完成分析并通过指定工具提交：\n" + _compact_json(facts),
            },
        ],
        "tools": [build_hy3_tool_definition()],
        "tool_choice": {
            "type": "function",
            "function": {"name": "submit_liquidity_analysis"},
        },
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "temperature": 0.1,
    }


def _extract_candidate(response: Dict[str, Any]) -> Dict[str, Any]:
    choices = response.get("choices") or []
    if not choices:
        raise ValueError("HY3 响应缺少 choices")
    message = choices[0].get("message") or {}
    for call in message.get("tool_calls") or []:
        function = call.get("function") or {}
        if function.get("name") != "submit_liquidity_analysis":
            continue
        arguments = function.get("arguments")
        if isinstance(arguments, str):
            return json.loads(arguments)
        if isinstance(arguments, dict):
            return arguments
    content = message.get("content")
    if isinstance(content, str) and content.strip():
        return json.loads(content)
    raise ValueError("HY3 响应中没有 submit_liquidity_analysis 工具参数或 JSON content")


def call_hy3(
    model_input: Dict[str, Any],
    api_key: str,
    endpoint: str = DEFAULT_ENDPOINT,
    model: str = DEFAULT_MODEL,
    timeout: int = 180,
) -> Dict[str, Any]:
    request_payload = build_request_payload(model_input, model=model)
    request = urllib.request.Request(
        endpoint,
        data=_compact_json(request_payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HY3 HTTP {exc.code}: {detail[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"HY3 请求失败: {exc.reason}") from exc
    return _extract_candidate(json.loads(body))


def _write_candidate(candidate: Dict[str, Any], directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    fd, raw_path = tempfile.mkstemp(prefix="analysis_candidate_", suffix=".json", dir=str(directory))
    path = Path(raw_path)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(candidate, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def parse_args(argv: List[str]) -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Call HY3 and atomically publish validated USD-liquidity analysis")
    parser.add_argument("--model-input", default=str(root / "output" / "latest" / "model_input.json"))
    parser.add_argument("--output", default=str(root / "output" / "latest" / "analysis.json"))
    parser.add_argument("--endpoint", default=os.getenv("HY3_ENDPOINT", DEFAULT_ENDPOINT))
    parser.add_argument("--model", default=os.getenv("HY3_MODEL", DEFAULT_MODEL))
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--dry-run", action="store_true", help="Only print request size and schema metadata; do not call HY3")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    model_input_path = Path(args.model_input).resolve()
    output_path = Path(args.output).resolve()
    model_input = json.loads(model_input_path.read_text(encoding="utf-8"))
    request_payload = build_request_payload(model_input, model=args.model)
    request_bytes = len(_compact_json(request_payload).encode("utf-8"))

    if args.dry_run:
        print(json.dumps({
            "model": args.model,
            "endpoint": args.endpoint,
            "request_bytes": request_bytes,
            "tool": "submit_liquidity_analysis",
            "will_publish_to": str(output_path),
        }, ensure_ascii=False))
        return 0

    api_key = os.getenv("TOKENHUB_API_KEY") or os.getenv("HY3_API_KEY")
    if not api_key:
        raise SystemExit("缺少 TOKENHUB_API_KEY 或 HY3_API_KEY 环境变量")

    candidate = call_hy3(
        model_input=model_input,
        api_key=api_key,
        endpoint=args.endpoint,
        model=args.model,
        timeout=args.timeout,
    )
    candidate_path = _write_candidate(candidate, output_path.parent)
    try:
        errors = publish_analysis_candidate(candidate_path, output_path, model_input_path)
    finally:
        candidate_path.unlink(missing_ok=True)
    if errors:
        print(json.dumps({"status": "validation_failed", "errors": errors}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({"status": "published", "output": str(output_path), "request_bytes": request_bytes}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
