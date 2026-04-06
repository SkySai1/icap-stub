"""Business logic for building ICAP responses."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ResponsePlan:
    """Plan for constructing a response."""

    status_code: int
    delay_ms: int


class ResponseBuilder:
    """Build ICAP response bytes for a given plan."""

    def build(self, plan: ResponsePlan) -> bytes:
        """Return ICAP response bytes based on the plan."""

        status_text = "OK" if plan.status_code == 200 else "Stub"
        now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        lines = [
            f"ICAP/1.0 {plan.status_code} {status_text}",
            f"Date: {now}",
            "Server: ICAP-Stub",
            "Connection: close",
            "",
            "",
        ]
        return "\r\n".join(lines).encode("ascii")
