"""
Client helpers for interacting with the AuditLog contract via Ape.

These utilities provide a thin abstraction so scripts, APIs, and tests can
submit log entries or fetch historical records without duplicating Ape wiring.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from ape import accounts, project
from ape.api.accounts import AccountAPI
from ape.contracts import ContractInstance

AUDIT_LOG_ADDRESS_ENV = "AUDIT_LOG_ADDRESS"
APE_ACCOUNT_ALIAS_ENV = "APE_ACCOUNT_ALIAS"


@dataclass
class LogPayload:
    """Structured audit event payload."""

    verb: str
    payload_hash: str
    ref_id: str
    metadata: Dict[str, Any] | None = None


def submit_log(
    payload: LogPayload,
    *,
    sender: AccountAPI | None = None,
    contract: ContractInstance | None = None,
    account_alias: str | None = None,
    contract_address: str | None = None,
) -> str:
    """
    Submit a log entry to the AuditLog contract and return the tx hash.
    """

    contract_instance = contract or _get_contract(contract_address)
    sender_account = sender or _get_account(account_alias)

    receipt = contract_instance.writeLog(
        payload.verb,
        _normalize_payload_hash(payload.payload_hash),
        payload.ref_id,
        sender=sender_account,
    )

    return _coerce_tx_hash(receipt)


def fetch_logs(
    *,
    limit: int | None = None,
    contract: ContractInstance | None = None,
    contract_address: str | None = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve recent log entries from the AuditLog contract.
    """

    contract_instance = contract or _get_contract(contract_address)
    total = contract_instance.totalLogs()
    if total == 0:
        return []

    start_index = 0
    if limit is not None:
        start_index = max(total - limit, 0)

    entries: List[Dict[str, Any]] = []
    for idx in range(start_index, total):
        log = contract_instance.getLog(idx)
        entries.append(
            {
                "index": idx,
                "actor": getattr(log, "actor"),
                "payload_hash": _format_bytes32(getattr(log, "payloadHash")),
                "verb": getattr(log, "verb"),
                "timestamp": int(getattr(log, "timestamp")),
                "ref_id": getattr(log, "refId"),
            }
        )

    return entries


def load_pending_entries(source: str) -> Iterable[LogPayload]:
    """
    Placeholder for future ingestion logic that reads pending entries from
    a file, queue, or REST payload.
    """

    raise NotImplementedError(f"load_pending_entries for source '{source}' is not implemented yet")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _get_account(account_alias: str | None = None) -> AccountAPI:
    alias = account_alias or os.getenv(APE_ACCOUNT_ALIAS_ENV)
    if not alias:
        raise RuntimeError(
            "No Ape account alias provided. Set APE_ACCOUNT_ALIAS or "
            "pass account_alias=.../sender=... to submit_log()."
        )

    return accounts.load(alias)


def _get_contract(contract_address: str | None = None) -> ContractInstance:
    address = contract_address or os.getenv(AUDIT_LOG_ADDRESS_ENV)
    if not address:
        raise RuntimeError(
            "Missing AuditLog contract address. Set AUDIT_LOG_ADDRESS or "
            "pass contract_address=.../contract=... to the client helpers."
        )

    return project.AuditLog.at(address)


def _normalize_payload_hash(value: str) -> str:
    if not isinstance(value, str) or not value.startswith("0x"):
        raise ValueError("payload_hash must be a 0x-prefixed hex string")
    if len(value) != 66:
        raise ValueError("payload_hash must represent 32 bytes (64 hex chars)")
    return value


def _format_bytes32(value: Any) -> str:
    if hasattr(value, "hex"):
        return value.hex()
    return str(value)


def _coerce_tx_hash(receipt: Any) -> str:
    tx_hash = getattr(receipt, "txn_hash", None) or getattr(receipt, "tx_hash", None)
    if tx_hash is None:
        raise RuntimeError("Transaction receipt did not include a hash")
    if hasattr(tx_hash, "hex"):
        hex_str = tx_hash.hex()
        if not hex_str.startswith("0x"):
            hex_str = "0x" + hex_str
        return hex_str
    if isinstance(tx_hash, str) and not tx_hash.startswith("0x"):
        return "0x" + tx_hash
    return str(tx_hash)
