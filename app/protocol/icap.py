"""ICAP protocol helpers."""

from __future__ import annotations


def read_request(data: bytes) -> str:
    """Decode incoming request bytes to a safe string for logging."""

    try:
        return data.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="replace")


def parse_request_line(request_text: str) -> tuple[str, str]:
    """Parse ICAP request line into method and service name."""

    if not request_text:
        return "", ""

    first_line = request_text.splitlines()[0].strip()
    if not first_line:
        return "", ""

    parts = first_line.split()
    if len(parts) < 2:
        return "", ""

    method = parts[0].upper()
    uri = parts[1]
    if "/" not in uri:
        return method, ""

    service = uri.rsplit("/", 1)[-1]
    if "?" in service:
        service = service.split("?", 1)[0]

    return method, service
