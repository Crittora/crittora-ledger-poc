"""
Client helpers for interacting with the AuditLog contract via Ape.

This module will eventually encapsulate account loading, transaction submission,
and event reconciliation logic. For now it provides type scaffolding so other
components (API, CLI, tests) can reference a consistent interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


@dataclass
class LogPayload:
    """Structured audit event payload."""

    verb: str
    payload_hash: str
    ref_id: str
    metadata: Dict[str, Any] | None = None


def submit_log(payload: LogPayload) -> str:
    """
    Submit a log entry to the AuditLog contract and return the tx hash.

    TODO: Implement Ape account loading and contract call once the contract
    interface is finalized.
    """

    raise NotImplementedError("submit_log will be implemented when contract deployment is available")


def fetch_logs(limit: int | None = None) -> List[Dict[str, Any]]:
    """
    Retrieve recent log entries from the AuditLog contract.

    TODO: Query on-chain events and transform them into friendly dicts.
    """

    raise NotImplementedError("fetch_logs will be implemented after contract deployment")


def load_pending_entries(source: str) -> Iterable[LogPayload]:
    """
    Placeholder for future ingestion logic that reads pending entries from
    a file, queue, or REST payload.
    """

    raise NotImplementedError(f"load_pending_entries for source '{source}' is not implemented yet")
