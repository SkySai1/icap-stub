"""Tests for ICAP protocol helpers."""

from __future__ import annotations

from app.protocol.icap import parse_request_line


def test_parse_request_line() -> None:
    """Should parse method and service name from request line."""

    method, service = parse_request_line("REQMOD icap://localhost/scan ICAP/1.0\r\n")

    assert method == "REQMOD"
    assert service == "scan"


def test_parse_request_line_strips_params() -> None:
    """Should strip params and normalize service name."""

    method, service = parse_request_line(
        "REQMOD icap://localhost/Scan;mode=reqmod?x=1 ICAP/1.0\r\n"
    )

    assert method == "REQMOD"
    assert service == "scan"
