"""Pytest configuration to ensure app package is importable."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest

from app.config.loader import ConfigLoader, ServerConfig


@pytest.fixture()
def test_config_path(tmp_path: Path) -> Path:
    """Create a temporary config file for tests."""

    config_path = tmp_path / ".test-config.ini"
    config_path.write_text(
        """
[server]
host = 127.0.0.1
log_level = DEBUG
default_response_code = 404
default_response_delay_ms = 0

[service:scan]
port = 1344
method = REQMOD
response_code = 204
response_delay_ms = 5

[service:rewrite]
port = 1344
method = RESPMOD
response_code = 201
response_delay_ms = 10
""".strip()
    )
    return config_path


@pytest.fixture()
def test_config(test_config_path: Path) -> ServerConfig:
    """Load the temporary test configuration."""

    return ConfigLoader().load(test_config_path)
