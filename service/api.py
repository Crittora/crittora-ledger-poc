"""
FastAPI surface for submitting and querying audit log entries.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from service import client


app = FastAPI(title="Crittora Ledger POC", version="0.1.0")


class LogRequest(BaseModel):
    verb: str
    payload_hash: str
    ref_id: str


class LogResponse(BaseModel):
    tx_hash: str


@app.post("/logs", response_model=LogResponse, status_code=status.HTTP_202_ACCEPTED)
def create_log(req: LogRequest) -> LogResponse:
    try:
        payload = client.LogPayload(verb=req.verb, payload_hash=req.payload_hash, ref_id=req.ref_id)
        tx_hash = client.submit_log(payload=payload)
        return LogResponse(tx_hash=tx_hash)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc


@app.get("/logs")
def list_logs(limit: int = 20):
    if limit <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="limit must be positive")

    try:
        entries = client.fetch_logs(limit=limit)
        return {"items": entries, "count": len(entries)}
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
