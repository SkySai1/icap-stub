"""Application entry point."""

from __future__ import annotations

from pathlib import Path

from app.config.loader import ConfigLoader
from app.handlers.port_handler import PortHandler
from app.server import IcapServer, ListeningPort


def build_server(config_path: Path) -> IcapServer:
    """Build the ICAP server from configuration."""

    loader = ConfigLoader()
    config = loader.load(config_path)

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
    server = build_server(config_path)
    server.start()


if __name__ == "__main__":
    main()
