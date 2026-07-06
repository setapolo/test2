import json
import tempfile
import unittest
from pathlib import Path

from scripts.create_request import create_request
from scripts.install_response import install_response
from scripts.process_request import process_request


class ExchangeTests(unittest.TestCase):
    def test_status_response_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            request_path = root / "request.json"
            response_path = root / "response.json"
            output_path = root / "api" / "response.json"

            create_request("status", request_path, run_id="123", run_attempt="2")
            process_request(request_path, response_path)
            installed = install_response(response_path, output_path, expected_id="123-2")

            self.assertEqual(installed["correlation_id"], "123-2")
            self.assertEqual(installed["type"], "status")
            self.assertEqual(installed["text"], "OK")
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), installed)

    def test_echo_response_does_not_execute_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            request_path = root / "request.json"
            response_path = root / "response.json"
            create_request("echo: $(touch should-not-exist)", request_path, run_id="1", run_attempt="1")
            response = process_request(request_path, response_path)

            self.assertEqual(response["type"], "echo")
            self.assertEqual(response["text"], "$(touch should-not-exist)")
            self.assertFalse((root / "should-not-exist").exists())

    def test_unknown_message_returns_ack(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            request_path = root / "request.json"
            response_path = root / "response.json"
            create_request("anything else", request_path, run_id="1", run_attempt="1")
            response = process_request(request_path, response_path)
            self.assertEqual(response["type"], "ack")
            self.assertEqual(response["text"], "ACK")

    def test_correlation_id_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            response_path = root / "response.json"
            response_path.write_text(json.dumps({"correlation_id": "wrong"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                install_response(response_path, root / "api" / "response.json", expected_id="expected")


if __name__ == "__main__":
    unittest.main()
