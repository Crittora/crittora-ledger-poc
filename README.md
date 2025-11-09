# Crittora Ledger POC

Minimal Ape/Python proof of concept that records audit events on Moonbeam networks (starting with Moonbase Alpha) to verify we can operate a public, append-only blockchain log.

## Objectives
- Prototype an `AuditLog` contract and Python service that submits structured events and returns verifiable tx hashes.
- Use only open-source tooling (Ape, Pytest, FastAPI/Typer) and keep the repo safe for public GitHub exposure.
- Validate the flow on Moonbase Alpha before pointing at Moonriver mainnet.

## Project Structure
```
contracts/        # Smart contracts (AuditLog.sol scaffold)
service/          # Python client/API helpers (placeholders for now)
scripts/          # CLI utilities for submit/fetch flows (Typer stubs)
tests/            # Pytest suites for contracts + service (skipped placeholders)
ape-config.yaml   # Ape project + network configuration
AGENTS.md         # Contributor guidelines
SRD.md            # System requirements & architecture plan
```

## Requirements
- Python 3.10+
- Ape Framework plus Moonbeam + Solidity plugins:
  ```bash
  pip install -r requirements.txt
  ape plugins install moonbeam solidity
  ```
- Solidity compiler 0.8.20 (managed automatically via `ape-config.yaml` once the plugin is installed).
- Local virtual environment (`python -m venv .venv && source .venv/bin/activate`)
- Moonbase Alpha account funded via the public faucet

## Setup
1. Clone the repo and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ape compile
   ```
2. Configure environment variables (never commit secrets):
   ```bash
   export MOONBASE_RPC_URL="https://rpc.api.moonbase.moonbeam.network"
   export PRIVATE_KEY="0xabc123..."          # or point Ape at an encrypted keyfile
   ```
3. Verify `ape-config.yaml` recognizes the Moonbase network (already scaffolded) and that your account is funded via the faucet.

## Useful Commands
- `ape compile` – compile contracts in `contracts/`.
- `ape test --network moonbeam:moonbase` – run Pytest suites against Moonbase Alpha (or omit `--network` for local testing).
- `ape run scripts/submit_log.py --network moonbeam:moonbase` – broadcast a demo audit event (script to be implemented).
- `ape run scripts/fetch_logs.py --network moonbeam:moonbase` – pull on-chain events for reconciliation.

## Security & Public Repo Hygiene
- Secrets (RPC URLs with credentials, private keys) must stay in environment variables or encrypted keyfiles ignored by Git.
- Run a secret scan before every push: `git secrets --scan`.
- See `AGENTS.md` for coding, testing, and PR expectations plus public-repo rules.

## Planning & Next Steps
The detailed requirements, open questions, and directory layout live in `SRD.md`. Current code is scaffolding only (API/CLI return 501/placeholder outputs). Next iterations should:
1. Implement the `AuditLog` contract storage + events.
2. Wire `service.client` to submit/read logs via Ape.
3. Connect the CLI/REST layers and flesh out the Pytest suites.
Track decisions and follow-ups in issues referencing the SRD sections.
