"""Tests for port handler logic."""

from __future__ import annotations

from app.config.loader import ServerConfig
from app.handlers.port_handler import PortHandler, ServiceRoute
from app.services.response_builder import ResponsePlan


def _build_handler(config: ServerConfig, port: int) -> PortHandler:
    """Build a port handler from the test config for a specific port."""

    services: dict[str, ServiceRoute] = {}
    for service in config.services:
        if service.port != port:
            continue
        services[service.name] = ServiceRoute(
            plan=ResponsePlan(
                status_code=service.response_code,
                delay_ms=service.response_delay_ms,
            ),
            reqmod=service.reqmod,
            respmod=service.respmod,
        )

    return PortHandler(
        port=port,
        services=services,
        default_plan=ResponsePlan(
            status_code=config.default_response_code,
            delay_ms=config.default_response_delay_ms,
        ),
    )


def test_plan_response_default(test_config: ServerConfig) -> None:
    """Port handler should fall back to default response plan."""

    handler = _build_handler(test_config, port=1344)
    plan, _requested, resolved = handler.plan_response("")

    assert plan.status_code == test_config.default_response_code
    assert plan.delay_ms == test_config.default_response_delay_ms
    assert resolved is None


def test_plan_response_reqmod_service(test_config: ServerConfig) -> None:
    """Port handler should return service response for REQMOD."""

    handler = _build_handler(test_config, port=1344)
    plan, requested, resolved = handler.plan_response(
        "REQMOD icap://localhost/scan ICAP/1.0\r\n\r\n"
    )

    assert plan.status_code == 204
    assert plan.delay_ms == 5
    assert requested == "scan"
    assert resolved == "scan"


def test_plan_response_respmod_service(test_config: ServerConfig) -> None:
    """Port handler should return service response for RESPMOD."""

    handler = _build_handler(test_config, port=1344)
    plan, requested, resolved = handler.plan_response(
        "RESPMOD icap://localhost/rewrite ICAP/1.0\r\n\r\n"
    )

    assert plan.status_code == 201
    assert plan.delay_ms == 10
    assert requested == "rewrite"
    assert resolved == "rewrite"


def test_plan_response_options_service(test_config: ServerConfig) -> None:
    """Port handler should resolve service for OPTIONS."""

    handler = _build_handler(test_config, port=1344)
    plan, requested, resolved = handler.plan_response(
        "OPTIONS icap://localhost/scan ICAP/1.0\r\n\r\n"
    )

    assert plan.status_code == 204
    assert plan.delay_ms == 5
    assert requested == "scan"
    assert resolved == "scan"
