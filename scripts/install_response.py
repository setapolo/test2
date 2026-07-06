#!/usr/bin/env python3
"""Validate and install the workflow response for GitHub Pages."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def expected_correlation_id(run_id: str | None = None, run_attempt: str | None = None) -> str:
    run_id = run_id if run_id is not None else os.environ.get("GITHUB_RUN_ID", "local")
    run_attempt = run_attempt if run_attempt is not None else os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    return f"{run_id}-{run_attempt}"


def install_response(response_path: Path, output_path: Path, expected_id: str | None = None) -> dict[str, str]:
    response = json.loads(response_path.read_text(encoding="utf-8"))
    expected = expected_id or expected_correlation_id()
    actual = response.get("correlation_id")
    if actual != expected:
        raise ValueError(f"response correlation_id mismatch: expected {expected!r}, got {actual!r}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate response.json and install it for Pages.")
    parser.add_argument("--response", default="response.json", help="Input response JSON path.")
    parser.add_argument("--output", default="api/response.json", help="Published response JSON path.")
    args = parser.parse_args()
    install_response(Path(args.response), Path(args.output))


if __name__ == "__main__":
    main()
