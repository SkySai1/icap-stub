"""Handlers that apply port-specific response logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from app.protocol.icap import parse_request_line
from app.services.response_builder import ResponsePlan


@dataclass(frozen=True)
class PortHandler:
    """Port-specific logic for ICAP responses."""

    port: int
    services: dict[str, dict[str, ResponsePlan]]
    default_plan: ResponsePlan

    def plan_response(self, request_text: str) -> tuple[ResponsePlan, str, Optional[str]]:
        """Return response plan with requested and resolved service names."""

        method, service = parse_request_line(request_text)
        if method in self.services and service in self.services[method]:
            return self.services[method][service], service, service

        return self.default_plan, service, None
