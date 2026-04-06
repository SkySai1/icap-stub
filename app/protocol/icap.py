"""ICAP protocol helpers."""

from __future__ import annotations


def read_request(data: bytes) -> str:
    """Decode incoming request bytes to a safe string for logging."""

    try:
        return data.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="replace")
