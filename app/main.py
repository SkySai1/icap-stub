"""Application entry point."""

from __future__ import annotations

from pathlib import Path

from app.config.loader import ConfigLoader, ServerConfig
from app.handlers.port_handler import PortHandler
from app.server import IcapServer, ListeningPort
from app.services.logging_setup import configure_logging


def build_server(config: ServerConfig) -> IcapServer:
    """Build the ICAP server from configuration."""

    ports = [
        ListeningPort(
            host=config.host,
            handler=PortHandler(
                port=port_config.port,
                response_code=port_config.response_code,
                response_delay_ms=port_config.response_delay_ms,
            ),
        )
        for port_config in config.ports
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
