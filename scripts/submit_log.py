"""
CLI utility for submitting audit log entries via Ape.

Executed with `ape run scripts/submit_log.py --network moonbeam:moonbase`.
Currently acts as a placeholder until the AuditLog contract and client helpers
are implemented.
"""

from __future__ import annotations

import typer

from service import client

app = typer.Typer(help="Submit an audit log entry to the Moonbase Alpha contract.")


@app.command()
def log(
    verb: str = typer.Argument(..., help="Action verb describing the event (e.g., CREATE)."),
    payload_hash: str = typer.Argument(..., help="0x-prefixed keccak or content hash."),
    ref_id: str = typer.Argument(..., help="External reference ID correlating to off-chain data."),
    account_alias: str = typer.Option(
        None,
        "--account-alias",
        "-a",
        help="Ape account alias used to sign the transaction. Defaults to $APE_ACCOUNT_ALIAS.",
    ),
    contract_address: str = typer.Option(
        None,
        "--contract-address",
        "-c",
        help="AuditLog contract address. Defaults to $AUDIT_LOG_ADDRESS.",
    ),
):
    payload = client.LogPayload(verb=verb, payload_hash=payload_hash, ref_id=ref_id)
    tx_hash = client.submit_log(
        payload,
        account_alias=account_alias,
        contract_address=contract_address,
    )
    typer.secho(f"Submitted audit log entry. tx={tx_hash}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
