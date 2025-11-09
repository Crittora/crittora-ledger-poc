"""
Utility script for fetching audit log entries from Moonbase Alpha.

Intended to run via `ape run scripts/fetch_logs.py --network moonbeam:moonbase`
once the AuditLog contract exposes read/query capabilities.
"""

from __future__ import annotations

from pathlib import Path

import typer

from service import client  # noqa: F401  # imported for future use

app = typer.Typer(help="Fetch audit log entries and write them to an artifact file.")


@app.command()
def export(limit: int = 100, output: Path = Path("artifacts/audit_snapshot.json")):
    typer.echo("Audit log export is not implemented yet.")
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
