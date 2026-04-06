"""Integration test using native sockets to send ICAP requests."""

from __future__ import annotations

import socket
import threading
import time
from pathlib import Path

import pytest

from app.config.loader import ConfigLoader
from app.main import build_server


def _get_free_port() -> int:
    """Find a free TCP port for test server."""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]
    except PermissionError as exc:
        pytest.skip(f"Socket operations not permitted in this environment: {exc}")


def _wait_for_port(host: str, port: int, timeout: float = 2.0) -> None:
    """Wait for a TCP port to accept connections."""

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.05)
    raise AssertionError(f"Port {host}:{port} did not open in time")


def _send_icap_request(host: str, port: int, request: str) -> str:
    """Send a raw ICAP request and return the response text."""

    with socket.create_connection((host, port), timeout=1.0) as sock:
        sock.sendall(request.encode("ascii"))
        response = sock.recv(4096)
    return response.decode("ascii", errors="replace")


def test_reqmod_with_native_socket(tmp_path: Path) -> None:
    """Should return configured response for REQMOD service."""

    port = _get_free_port()
    config_path = tmp_path / ".test-config.ini"
    config_path.write_text(
        f"""
[server]
host = 127.0.0.1
log_level = INFO
default_response_code = 404
default_response_delay_ms = 0

[service:scan]
port = {port}
reqmod = true
respmod = false
response_code = 204
response_delay_ms = 0
""".strip()
    )
    config = ConfigLoader().load(config_path)
    server = build_server(config)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()

    _wait_for_port("127.0.0.1", port)

    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("hello")

    request = (
        "REQMOD icap://localhost/scan ICAP/1.0\r\n"
        "Host: localhost\r\n"
        "Allow: 204\r\n"
        "\r\n"
    )

    response = _send_icap_request("127.0.0.1", port, request)

    assert response.startswith("ICAP/1.0 200")
    assert "Encapsulated: res-hdr=0\r\n" in response
    assert "HTTP/1.1 204 No Content\r\n" in response


def test_options_returns_methods_header(tmp_path: Path) -> None:
    """OPTIONS response should include available ICAP methods."""

    port = _get_free_port()
    config_path = tmp_path / ".test-config.ini"
    config_path.write_text(
        f"""
[server]
host = 127.0.0.1
log_level = INFO
default_response_code = 404
default_response_delay_ms = 0

[service:scan]
port = {port}
reqmod = true
respmod = true
response_code = 200
response_delay_ms = 0
""".strip()
    )
    config = ConfigLoader().load(config_path)
    server = build_server(config)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()

    _wait_for_port("127.0.0.1", port)

    request = "OPTIONS icap://localhost/scan ICAP/1.0\r\n\r\n"
    response = _send_icap_request("127.0.0.1", port, request)

    assert "Methods: REQMOD, RESPMOD\r\n" in response
