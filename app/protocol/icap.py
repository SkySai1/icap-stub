"""ICAP protocol helpers."""

from __future__ import annotations

from urllib.parse import unquote, urlparse


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
    parsed = urlparse(uri)
    if parsed.scheme and parsed.path:
        path = parsed.path.strip("/")
        service = path.split("/")[-1] if path else ""
        return method, unquote(service).lower()

    if "/" not in uri:
        return method, ""

    service = uri.rsplit("/", 1)[-1]
    if "?" in service:
        service = service.split("?", 1)[0]
    if ";" in service:
        service = service.split(";", 1)[0]

    return method, unquote(service).lower()


def parse_request_details(request_text: str) -> tuple[str, str, str, list[tuple[str, str]]]:
    """Parse request line and headers for detailed logging."""

    if not request_text:
        return "", "", "", []

    lines = request_text.splitlines()
    if not lines:
        return "", "", "", []

    first_line = lines[0].strip()
    parts = first_line.split()
    method = parts[0].upper() if len(parts) > 0 else ""
    uri = parts[1] if len(parts) > 1 else ""
    version = parts[2] if len(parts) > 2 else ""

    headers: list[tuple[str, str]] = []
    for line in lines[1:]:
        if not line.strip():
            break
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        headers.append((name.strip(), value.strip()))

    return method, uri, version, headers
