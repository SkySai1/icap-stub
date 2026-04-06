"""Business logic for building ICAP responses."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Iterable


@dataclass(frozen=True)
class ResponsePlan:
    """Plan for constructing a response."""

    status_code: int
    delay_ms: int


class ResponseBuilder:
    """Build ICAP response bytes for a given plan."""

    def build(
        self,
        plan: ResponsePlan,
        extra_headers: Iterable[str] | None = None,
        include_http_response: bool = False,
        icap_status_code: int = 200,
    ) -> bytes:
        """Return ICAP response bytes based on the plan."""

        status_text = self._status_text(icap_status_code)
        now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        lines = [
            f"ICAP/1.0 {icap_status_code} {status_text}",
            f"Date: {now}",
            "Server: ICAP-Stub",
            "Connection: close",
        ]
        if include_http_response:
            lines.append("Encapsulated: res-hdr=0")
        if extra_headers:
            lines.extend(extra_headers)
        lines.extend(["", ""])
        response = "\r\n".join(lines).encode("ascii")
        if not include_http_response:
            return response

        http_response = self._build_http_response(plan.status_code, now)
        return response + http_response

    @staticmethod
    def _status_text(status_code: int) -> str:
        """Return standard reason phrase for the status code."""

        try:
            return HTTPStatus(status_code).phrase
        except ValueError:
            return "Stub"

    @staticmethod
    def _build_http_response(status_code: int, date_value: str) -> bytes:
        """Return an HTTP response payload for ICAP encapsulation."""

        reason = ResponseBuilder._status_text(status_code)
        lines = [
            f"HTTP/1.1 {status_code} {reason}",
            f"Date: {date_value}",
            "Server: ICAP-Stub",
            "Content-Length: 0",
            "Connection: close",
            "",
            "",
        ]
        return "\r\n".join(lines).encode("ascii")
