#!/usr/bin/env python3
"""Process request.json into response.json without executing user input."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_response(message: str) -> dict[str, str]:
    if message == "status":
        return {"type": "status", "text": "OK"}
    if message.startswith("echo: "):
        return {"type": "echo", "text": message.removeprefix("echo: ")}
    return {"type": "ack", "text": "ACK"}


def process_request(request_path: Path, output_path: Path) -> dict[str, str]:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    correlation_id = request.get("correlation_id")
    message = request.get("message", "")
    if not isinstance(correlation_id, str) or not correlation_id:
        raise ValueError("request.json must include a non-empty string correlation_id")
    if not isinstance(message, str):
        raise ValueError("request.json message must be a string")

    response = {"correlation_id": correlation_id, **build_response(message)}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Process request.json into response.json.")
    parser.add_argument("--request", default="request.json", help="Input request JSON path.")
    parser.add_argument("--output", default="response.json", help="Output response JSON path.")
    args = parser.parse_args()
    process_request(Path(args.request), Path(args.output))


if __name__ == "__main__":
    main()
