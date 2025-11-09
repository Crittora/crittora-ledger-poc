"""
Service package for interacting with the AuditLog contract via Ape.

Modules:
    client: High-level helpers for submitting and fetching log entries.
    api: FastAPI surface (thin wrapper around client helpers).

Both modules are imported lazily to avoid forcing FastAPI as a dependency
when only the client helper is needed (e.g., during unit tests).
"""

from importlib import import_module
from types import ModuleType
from typing import Any, Dict

__all__ = ["client", "api"]

_CACHE: Dict[str, ModuleType] = {}


def __getattr__(name: str) -> Any:
    if name not in __all__:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    if name not in _CACHE:
        _CACHE[name] = import_module(f".{name}", __name__)
    return _CACHE[name]
