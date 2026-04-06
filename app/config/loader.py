"""Configuration loading utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import configparser


@dataclass(frozen=True)
class ServiceConfig:
    """Configuration for a single ICAP service."""

    name: str
    port: int
    method: str
    response_code: int
    response_delay_ms: int


@dataclass(frozen=True)
class ServerConfig:
    """Top-level server configuration."""

    host: str
    log_level: str
    default_response_code: int
    default_response_delay_ms: int
    services: list[ServiceConfig]


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

        default_response_code = parser.getint(
            "server", "default_response_code", fallback=404
        )
        default_response_delay_ms = parser.getint(
            "server", "default_response_delay_ms", fallback=0
        )

        services: list[ServiceConfig] = []
        for section in parser.sections():
            if not section.startswith("service:"):
                continue
            service_name = section.split(":", 1)[1].strip()
            if not service_name:
                raise ValueError("Service name must be provided in section header.")

            port_number = parser.getint(section, "port")
            response_code = parser.getint(section, "response_code", fallback=200)
            response_delay_ms = parser.getint(section, "response_delay_ms", fallback=0)
            method = parser.get(section, "method", fallback="REQMOD").upper()

            if method not in {"REQMOD", "RESPMOD"}:
                raise ValueError(
                    "Service method must be REQMOD or RESPMOD, got "
                    f"'{method}'."
                )

            services.append(
                ServiceConfig(
                    name=service_name,
                    port=port_number,
                    method=method,
                    response_code=response_code,
                    response_delay_ms=response_delay_ms,
                )
            )

        if not services:
            raise ValueError("At least one [service:<name>] section is required")

        return ServerConfig(
            host=host,
            log_level=log_level,
            default_response_code=default_response_code,
            default_response_delay_ms=default_response_delay_ms,
            services=services,
        )
