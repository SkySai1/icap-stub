"""Tests for configuration loading."""

from __future__ import annotations

from pathlib import Path

from app.config.loader import ConfigLoader


def test_load_config(tmp_path: Path) -> None:
    """Config loader should parse server and port settings."""

    config_path = tmp_path / "config.ini"
    config_path.write_text(
        """
[server]
host = 127.0.0.1
log_level = DEBUG

[port:1344]
response_code = 204
response_delay_ms = 10
""".strip()
    )

    config = ConfigLoader().load(config_path)

    assert config.host == "127.0.0.1"
    assert config.log_level == "DEBUG"
    assert len(config.ports) == 1
    port = config.ports[0]
    assert port.port == 1344
    assert port.response_code == 204
    assert port.response_delay_ms == 10
