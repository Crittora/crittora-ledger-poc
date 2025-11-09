"""
Utility script for fetching audit log entries from Moonbase Alpha.

Intended to run via `ape run scripts/fetch_logs.py --network moonbeam:moonbase`
once the AuditLog contract exposes read/query capabilities.
"""

from __future__ import annotations

from pathlib import Path
import json

import typer

from service import client


def main(
    limit: int = typer.Option(100, help="Maximum number of most recent entries to fetch."),
    output: Path = typer.Option(Path("artifacts/audit_snapshot.json"), help="File path for the exported JSON."),
    contract_address: str | None = typer.Option(
        None,
        "--contract-address",
        "-c",
        help="AuditLog contract address. Defaults to $AUDIT_LOG_ADDRESS.",
    ),
) -> None:
    entries = client.fetch_logs(limit=limit, contract_address=contract_address)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(entries, indent=2))
    typer.secho(f"Wrote {len(entries)} entries to {output}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    typer.run(main)
