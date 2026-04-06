"""Handlers that apply port-specific response logic."""

from __future__ import annotations

from dataclasses import dataclass
from app.protocol.icap import parse_request_line
from app.services.response_builder import ResponsePlan


@dataclass(frozen=True)
class PortHandler:
    """Port-specific logic for ICAP responses."""

    port: int
    services: dict[str, dict[str, ResponsePlan]]
    default_plan: ResponsePlan

    def plan_response(self, request_text: str) -> ResponsePlan:
        """Return a response plan derived from the request and config."""

        method, service = parse_request_line(request_text)
        if method in self.services and service in self.services[method]:
            return self.services[method][service]

        return self.default_plan
