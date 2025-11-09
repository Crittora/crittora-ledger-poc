"""
FastAPI surface for submitting and querying audit log entries.

The implementation intentionally returns HTTP 501 (Not Implemented) until the
underlying client primitives are wired up. This keeps the API contract visible
while preventing accidental usage.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from service import client  # noqa: F401  # imported for future use


app = FastAPI(title="Crittora Ledger POC", version="0.1.0")


class LogRequest(BaseModel):
    verb: str
    payload_hash: str
    ref_id: str


class LogResponse(BaseModel):
    tx_hash: str


@app.post("/logs", response_model=LogResponse, status_code=status.HTTP_202_ACCEPTED)
def create_log(req: LogRequest) -> LogResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="submit_log API will be enabled once the AuditLog contract is deployed",
    )


@app.get("/logs")
def list_logs(limit: int = 20):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="fetch_logs API will be enabled once the AuditLog contract is deployed",
    )
