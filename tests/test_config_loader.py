"""Tests for configuration loading."""

from __future__ import annotations

from pathlib import Path

from app.config.loader import ConfigLoader


def test_load_config(tmp_path: Path) -> None:
    """Config loader should parse server and port settings."""

    config_path = tmp_path / ".test-config.ini"
    config_path.write_text(
        """
[server]
host = 127.0.0.1
log_level = DEBUG
default_response_code = 418
default_response_delay_ms = 7

[service:scan]
port = 1344
reqmod = true
respmod = false
response_code = 204
response_delay_ms = 10
[service:rewrite]
port = 1344
reqmod = false
respmod = true
response_code = 201
response_delay_ms = 5
""".strip()
    )

    config = ConfigLoader().load(config_path)

    assert config.host == "127.0.0.1"
    assert config.log_level == "DEBUG"
    assert config.default_response_code == 418
    assert config.default_response_delay_ms == 7
    assert len(config.services) == 2

    service = config.services[0]
    assert service.name == "scan"
    assert service.port == 1344
    assert service.reqmod is True
    assert service.respmod is False
    assert service.response_code == 204
    assert service.response_delay_ms == 10

    service = config.services[1]
    assert service.name == "rewrite"
    assert service.port == 1344
    assert service.reqmod is False
    assert service.respmod is True
    assert service.response_code == 201
    assert service.response_delay_ms == 5
