"""Configuration loading utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import configparser


@dataclass(frozen=True)
class PortConfig:
    """Configuration for a single ICAP port."""

    port: int
    response_code: int
    response_delay_ms: int


@dataclass(frozen=True)
class ServerConfig:
    """Top-level server configuration."""

    host: str
    log_level: str
    ports: list[PortConfig]


class ConfigLoader:
    """Load server configuration from an INI file."""

    def load(self, path: Path) -> ServerConfig:
        """Parse and return a structured server configuration."""

        parser = configparser.ConfigParser()
        read_files = parser.read(path)
        if not read_files:
            raise FileNotFoundError(f"Config file not found: {path}")

        if "server" not in parser:
            raise ValueError("Missing [server] section in config.ini")

        host = parser.get("server", "host", fallback="0.0.0.0")
        log_level = parser.get("server", "log_level", fallback="INFO")

        ports: list[PortConfig] = []
        for section in parser.sections():
            if not section.startswith("port:"):
                continue
            port_number = int(section.split(":", 1)[1])
            response_code = parser.getint(section, "response_code", fallback=200)
            response_delay_ms = parser.getint(section, "response_delay_ms", fallback=0)
            ports.append(
                PortConfig(
                    port=port_number,
                    response_code=response_code,
                    response_delay_ms=response_delay_ms,
                )
            )

        if not ports:
            raise ValueError("At least one [port:<number>] section is required")

        return ServerConfig(host=host, log_level=log_level, ports=ports)
