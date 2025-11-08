# System Requirements Document (SRD)

## 1. Purpose & Vision
Build a minimal, open-source service that records immutable audit events on Moonriver by first proving the flow on the Moonbase Alpha testnet. The service must expose a simple interface for upstream systems to log actions, rely on Ape + Python for all on-chain interactions, and produce verifiable evidence (Tx hashes, event logs) that can be reconciled off-chain.

## 2. Scope
- **In scope:** smart-contract audit log, Ape-based service scripts, optional REST layer, Moonbase Alpha deployment pipeline, test coverage, documentation.
- **Out of scope:** UI dashboards, proprietary analytics, custodial key management, production Moonriver deployment (until Moonbase validation is complete).

## 3. Goals & Success Criteria
1. Submit structured audit events (actor, verb, payload hash, timestamp) to Moonbase Alpha within <3 seconds median latency.
2. Guarantee append-only history via contract storage + emitted events.
3. Provide a CLI or REST entry point returning Tx hash + event metadata.
4. Automate local testing and Moonbase deployment through reproducible Ape commands.

## 4. Constraints & Assumptions
- Entire codebase stays public; no proprietary IP or secrets committed.
- Use only open-source dependencies (Ape, FastAPI/Flask, Pytest, GitHub Actions, git-secrets).
- Keys live in env vars or encrypted keyfiles ignored by Git.
- Moonbase Alpha RPC endpoints are rate-limited; batching must respect provider limits.

## 5. Functional Requirements
- **F1 Contract:** `AuditLog` contract stores an array/map of events and emits `LogEntry(address actor, bytes32 payloadHash, string verb, uint256 timestamp, string refId)`.
- **F2 Submission Service:** Python module under `service/` exposes `submit_log(actor_alias, verb, payload)` that signs and broadcasts via Ape.
- **F3 REST/CLI:** Optional FastAPI app (`service/api.py`) or CLI (`scripts/submit_log.py`) accessible by other services.
- **F4 Reconciliation:** `scripts/fetch_logs.py` fetches on-chain events and saves to `./artifacts/audit_snapshot.json`.
- **F5 Config Management:** `ape-config.yaml` declares the Moonbeam plugin with `moonbeam:moonbase` network and points to RPC URL env var.

## 6. Non-Functional Requirements
- **Security:** No plaintext secrets; enforce `git secrets --scan` in CI. Require reviewers to confirm diffs are safe for a public repo.
- **Reliability:** Submission retries with exponential backoff; report failures without dropping events.
- **Performance:** Cap per-request runtime to <5 seconds including RPC confirmation; log queue should persist unsent entries locally.
- **Observability:** Structured logging (JSON) capturing request ID, tx hash, and status; nightly reconciliation job to detect divergence.

## 7. Architecture & Project Structure
```
contracts/
  AuditLog.sol        # append-only ledger
service/
  __init__.py
  client.py           # Ape helpers (load accounts, submit tx)
  api.py              # optional REST/FastAPI surface
scripts/
  submit_log.py       # CLI entry point
  fetch_logs.py       # reconciliation utility
tests/
  test_audit_log.py   # unit + property tests
  test_service.py     # integration against Moonbase mocks
ape-config.yaml       # networks, plugins, compilers
AGENTS.md, SRD.md     # contributor + requirements docs
```
All new directories must include `__init__.py` (even if empty) to remain importable.

## 8. Data Flow
1. Upstream system calls REST/CLI → service validates payload, hashes body.
2. Service loads Ape project context, signs tx with Moonbase Alpha account, submits via `moonbeam:moonbase`.
3. Contract writes event struct + emits event; tx hash returned.
4. Reconciliation script periodically pulls events, compares with off-chain ledger, and raises discrepancies.

## 9. Tooling & Dependencies
- Python 3.10+, Ape Framework (`ape`, `ape-moonbeam`, `ape-solidity`), `web3.py` (as needed).
- FastAPI + Uvicorn (REST), Rich/Typer (CLI), Pytest + Hypothesis.
- GitHub Actions: lint (`black`, `ruff`), tests (`ape test`), secret scanning (git-secrets or Gitleaks), contract compile check.

## 10. Testing Strategy
- **Contract:** Pytest unit tests + Hypothesis fuzzing for append-only guarantees, revert cases.
- **Service:** Mock Moonbase RPC for unit tests; integration tests hitting Moonbase Alpha nightly with funded test account.
- **End-to-end:** Scenario test running `submit_log` followed by `fetch_logs` to ensure parity.

## 11. Security & Compliance
- Enforce `.env.example` describing required env vars (RPC URL, PRIVATE_KEY) while `.env` is gitignored.
- Document key-rotation steps and faucet refills for Moonbase Alpha.
- Monitor contract upgradeability; if proxies used, require admin multi-sig (even on testnet) to reduce accidental changes.

## 12. Open Questions
1. Is REST exposure mandatory or will CLI suffice for MVP?
2. Should we persist full payloads off-chain or only hashed references?
3. What throughput is expected (events/minute) and do we need queuing?
4. How soon do we transition from Moonbase Alpha to Moonriver mainnet after validation?
