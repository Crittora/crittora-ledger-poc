"""
Deploy the AuditLog contract to the target Ape network.

Usage:
    ape run scripts/deploy_audit_log.py --network moonbeam:moonbase -- --account-alias ledger
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import typer
from ape import accounts, chain, project
from ape.api.accounts import AccountAPI

APE_ACCOUNT_ALIAS_ENV = "APE_ACCOUNT_ALIAS"
AUDIT_LOG_ENV_KEY = "AUDIT_LOG_ADDRESS"
AUDIT_LOG_ENV_PATH_ENV = "AUDIT_LOG_ENV_PATH"


def main() -> None:
    _deploy()


def _deploy(
    account_alias: Optional[str] = None,
    save_env: Optional[Path] = None,
    record: bool = True,
) -> None:
    sender = _load_account(account_alias)
    typer.secho(f"Deploying AuditLog with account {sender.alias!r}...", fg=typer.colors.CYAN)
    _emit_balance(sender)

    contract = project.AuditLog.deploy(sender=sender)
    if contract is None or not getattr(contract, "address", None):
        raise RuntimeError("AuditLog deployment failed; no contract address returned.")

    address = str(contract.address)

    typer.secho(f"AuditLog deployed to {address}", fg=typer.colors.GREEN)
    typer.echo(f"Set {AUDIT_LOG_ENV_KEY}={address} for client/API usage.")

    env_target = save_env or _resolve_env_path()
    if env_target:
        _append_env(env_target, address)
        typer.secho(f"Updated {env_target} with {AUDIT_LOG_ENV_KEY}={address}", fg=typer.colors.BLUE)

    if record:
        _write_deployment_record(address, sender.alias or sender.address)


def _load_account(alias_override: Optional[str]) -> AccountAPI:
    alias = alias_override or os.getenv(APE_ACCOUNT_ALIAS_ENV)
    if not alias:
        raise RuntimeError(
            f"No account alias provided. Pass --account-alias or set ${APE_ACCOUNT_ALIAS_ENV}."
        )
    return accounts.load(alias)


def _resolve_env_path() -> Optional[Path]:
    path = os.getenv(AUDIT_LOG_ENV_PATH_ENV)
    if path:
        return Path(path)
    default_env = Path(".env")
    return default_env if default_env.exists() else None


def _emit_balance(sender: AccountAPI) -> None:
    raw_balance = getattr(sender, "balance", None)
    if raw_balance is None:
        return
    dev_balance = raw_balance / 1e18
    typer.echo(f"Account balance: {dev_balance:.4f} DEV")


def _append_env(path: Path, address: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    if path.exists():
        lines = path.read_text().splitlines()
        lines = [line for line in lines if not line.startswith(f"{AUDIT_LOG_ENV_KEY}=")]
    lines.append(f"{AUDIT_LOG_ENV_KEY}={address}")
    path.write_text("\n".join(lines) + "\n")


def _write_deployment_record(address: str, alias: str) -> None:
    provider = chain.provider
    network_slug = f"{provider.network.ecosystem.name}-{provider.network.name}"
    output_dir = Path("artifacts/deployments")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    record_path = output_dir / f"{network_slug}.json"
    data = {
        "network": network_slug,
        "address": address,
        "deployer": alias,
        "timestamp": timestamp,
    }
    import json

    record_path.write_text(json.dumps(data, indent=2))
    typer.secho(f"Wrote deployment record to {record_path}", fg=typer.colors.BLUE)


def cli_entry(
    account_alias: Optional[str] = typer.Option(
        None, "--account-alias", "-a", help="Override $APE_ACCOUNT_ALIAS for deployment."
    ),
    save_env: Optional[Path] = typer.Option(
        None,
        "--save-env",
        help="Optional .env file to update with the new AUDIT_LOG_ADDRESS entry.",
    ),
    record: bool = typer.Option(
        True,
        "--record/--no-record",
        help="Write a JSON deployment record under artifacts/deployments/.",
    ),
) -> None:
    _deploy(account_alias, save_env, record)


if __name__ == "__main__":
    typer.run(cli_entry)
