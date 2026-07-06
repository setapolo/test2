#!/usr/bin/env python3
"""Create a request.json payload for the local GitHub Actions exchange."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def correlation_id(run_id: str | None = None, run_attempt: str | None = None) -> str:
    run_id = run_id if run_id is not None else os.environ.get("GITHUB_RUN_ID", "local")
    run_attempt = run_attempt if run_attempt is not None else os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    return f"{run_id}-{run_attempt}"


def create_request(message: str, output: Path, run_id: str | None = None, run_attempt: str | None = None) -> dict[str, str]:
    payload = {
        "correlation_id": correlation_id(run_id, run_attempt),
        "message": message,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Create request.json for the workflow exchange.")
    parser.add_argument("--message", default="status", help="Message to pass to the worker.")
    parser.add_argument("--output", default="request.json", help="Output request JSON path.")
    args = parser.parse_args()
    create_request(args.message, Path(args.output))


if __name__ == "__main__":
    main()
