"""
Service package for interacting with the AuditLog contract via Ape.

Modules:
    client: High-level helpers for submitting and fetching log entries.
    api: FastAPI surface (thin wrapper around client helpers).
"""

from service import api, client

__all__ = ["api", "client"]
