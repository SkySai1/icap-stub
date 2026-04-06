"""Tests for port handler logic."""

from __future__ import annotations

from app.handlers.port_handler import PortHandler


def test_plan_response() -> None:
    """Port handler should map config to response plan."""

    handler = PortHandler(port=1344, response_code=201, response_delay_ms=25)
    plan = handler.plan_response()

    assert plan.status_code == 201
    assert plan.delay_ms == 25
