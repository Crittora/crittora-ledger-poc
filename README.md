# Crittora Ledger POC

Minimal Ape/Python proof of concept that records audit events on Moonbeam networks (starting with Moonbase Alpha) to verify we can operate a public, append-only blockchain log.

## Objectives
- Prototype an `AuditLog` contract and Python service that submits structured events and returns verifiable tx hashes.
- Use only open-source tooling (Ape, Pytest, FastAPI/Typer) and keep the repo safe for public GitHub exposure.
- Validate the flow on Moonbase Alpha before pointing at Moonriver mainnet.

## Project Structure
```
contracts/        # Smart contracts (e.g., AuditLog.sol)
service/          # Python client/API helpers (to be added)
scripts/          # CLI utilities for submit/fetch flows
tests/            # Pytest suites for contracts + service
ape-config.yaml   # Ape project + network configuration
AGENTS.md         # Contributor guidelines
SRD.md            # System requirements & architecture plan
```

## Requirements
- Python 3.10+
- Ape Framework (`pip install ape`) plus Moonbeam + Solidity plugins:
  ```bash
  ape plugins install moonbeam solidity
  ```
- Local virtual environment (`python -m venv .venv && source .venv/bin/activate`)
- Moonbase Alpha account funded via the public faucet

## Setup
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt  # once defined
   ape compile
   ```
2. Configure environment variables (never commit secrets):
   ```bash
   export MOONBASE_RPC_URL="https://rpc.api.moonbase.moonbeam.network"
   export PRIVATE_KEY="0xabc123..."          # or point Ape at an encrypted keyfile
   ```
3. Update `ape-config.yaml` with the Moonbase network alias if not already present.

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
The detailed requirements, open questions, and directory layout live in `SRD.md`. Start by implementing the `AuditLog` contract, Moonbase config, and submission/reconciliation scripts, then incrementally add the service/API layer. Track decisions and follow-ups in issues referencing the SRD sections.
