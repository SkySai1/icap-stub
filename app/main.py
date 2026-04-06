"""Application entry point."""

from __future__ import annotations

from pathlib import Path

from app.config.loader import ConfigLoader, ServerConfig
from app.handlers.port_handler import PortHandler, ServiceRoute
from app.server import IcapServer, ListeningPort
from app.services.response_builder import ResponsePlan
from app.services.logging_setup import configure_logging


def build_server(config: ServerConfig) -> IcapServer:
    """Build the ICAP server from configuration."""

    services_by_port: dict[int, dict[str, ServiceRoute]] = {}
    for service in config.services:
        service_map = services_by_port.setdefault(service.port, {})
        service_map[service.name] = ServiceRoute(
            plan=ResponsePlan(
                status_code=service.response_code,
                delay_ms=service.response_delay_ms,
            ),
            reqmod=service.reqmod,
            respmod=service.respmod,
        )

    ports = [
        ListeningPort(
            host=config.host,
            handler=PortHandler(
                port=port,
                services=services,
                default_plan=ResponsePlan(
                    status_code=config.default_response_code,
                    delay_ms=config.default_response_delay_ms,
                ),
            ),
        )
        for port, services in services_by_port.items()
    ]

    return IcapServer(ports)


def main() -> None:
    """Run the ICAP stub server."""

    config_path = Path("config.ini")
    loader = ConfigLoader()
    config = loader.load(config_path)
    configure_logging(config.log_level)
    server = build_server(config)
    server.start()


if __name__ == "__main__":
    main()
