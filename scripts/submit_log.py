"""
CLI utility for submitting audit log entries via Ape.

Executed with `ape run scripts/submit_log.py --network moonbeam:moonbase`.
Currently acts as a placeholder until the AuditLog contract and client helpers
are implemented.
"""

from __future__ import annotations

import typer

from service import client  # noqa: F401  # imported for future use

app = typer.Typer(help="Submit an audit log entry to the Moonbase Alpha contract.")


@app.command()
def log(verb: str, payload_hash: str, ref_id: str):
    typer.echo("Audit log submission is not implemented yet.")
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
