"""Handlers that apply port-specific response logic."""

from __future__ import annotations

from dataclasses import dataclass
from app.services.response_builder import ResponsePlan


@dataclass(frozen=True)
class PortHandler:
    """Port-specific logic for ICAP responses."""

    port: int
    response_code: int
    response_delay_ms: int

    def plan_response(self) -> ResponsePlan:
        """Return a response plan derived from the port configuration."""

        return ResponsePlan(
            status_code=self.response_code,
            delay_ms=self.response_delay_ms,
        )
