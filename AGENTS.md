# Repository Guidelines

## Project Structure & Module Organization
Source follows the Ape layout: `contracts/` for Solidity/Vyper, `scripts/` for automation, `tests/` for Pytest. `ape-config.yaml` pins plugins, networks, and compilers. Keep artifacts and secrets out of Git; `.venv/` stays local.

## Build, Test, and Development Commands
- `ape compile` – rebuilds every contract; run after edits.
- `ape test` – runs the Pytest suite in `tests/`; add `-k <pattern>` to focus.
- `ape run scripts/<name>.py --network <alias>` – executes deployment or maintenance scripts against a target network.
- `ape console --network <alias>` – opens an interactive shell with project accounts.
Activate via `source .venv/bin/activate` before running Ape.

## Coding Style & Naming Conventions
Use 4-space indentation and snake_case for Python; reserve PascalCase for contracts and structs. Keep files cohesive—one contract or scenario per file—and comment only when logic is non-obvious. Format Python with `python -m black scripts tests`; for contracts, mirror the compiler formatter or run `ape fmt`. Name scripts after their action (`deploy_registry.py`, `snapshot_balances.py`) to aid discovery.

## Testing Guidelines
Mirror on-chain modules when organizing tests (`tests/test_registry.py`, `tests/compliance/`). Name cases `test_<behavior>_<expectation>` so failures explain themselves. Target ≥80% coverage on critical contracts, adding property-based or fuzz tests when invariants matter. Use Ape fixtures for clean states and add regression tests when bugs are fixed.

## Commit & Pull Request Guidelines
Adopt Conventional Commits (`feat:`, `fix:`, `chore:`) to keep history searchable. Each PR should include a short summary, test evidence (`ape test` output or a rationale for skipping), and linked issue references; attach screenshots or transaction hashes only when behavior changes. Scope PRs to one feature or fix per branch and rebase to avoid merge noise.

## Security & Configuration Tips
Never hard-code secrets, private keys, or proprietary IP; load sensitive values via environment variables consumed by Ape. Review `ape-config.yaml` before pointing at live networks, ensuring gas caps and deployment accounts are correct. When sharing traces or logs, sanitize addresses and transaction identifiers that could disclose customer data.

## Public Repository Hygiene
Treat every branch as world-readable. Run a secret scanner (`git secrets --scan` or similar) before pushing and rewrite history immediately if anything leaks. Keep `.gitignore` current so builds, traces, and configs stay local, and never commit partner assets or proprietary diagrams—store them privately and reference docs. Require reviewers to confirm diffs omit keys, mnemonics, endpoint URLs, or sensitive logic before merging.
