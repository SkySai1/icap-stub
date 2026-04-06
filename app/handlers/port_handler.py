"""Handlers that apply port-specific response logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from app.protocol.icap import parse_request_line
from app.services.response_builder import ResponsePlan


@dataclass(frozen=True)
class ServiceRoute:
    """Routing rules for a single service."""

    plan: ResponsePlan
    reqmod: bool
    respmod: bool


@dataclass(frozen=True)
class PortHandler:
    """Port-specific logic for ICAP responses."""

    port: int
    services: dict[str, ServiceRoute]
    default_plan: ResponsePlan

    def plan_response(
        self, request_text: str
    ) -> tuple[ResponsePlan, str, Optional[str], tuple[str, ...]]:
        """Return response plan plus requested/resolved service and allowed methods."""

        method, service = parse_request_line(request_text)
        route = self.services.get(service)
        if route:
            if method == "OPTIONS":
                return route.plan, service, service, self._allowed_methods(route)
            if method == "REQMOD" and route.reqmod:
                return route.plan, service, service, ()
            if method == "RESPMOD" and route.respmod:
                return route.plan, service, service, ()

        return self.default_plan, service, None, ()

    @staticmethod
    def _allowed_methods(route: ServiceRoute) -> tuple[str, ...]:
        """Return supported ICAP methods for a service in stable order."""

        methods: list[str] = []
        if route.reqmod:
            methods.append("REQMOD")
        if route.respmod:
            methods.append("RESPMOD")
        return tuple(methods)
