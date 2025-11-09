import json
from dataclasses import dataclass
from pathlib import Path

import pytest
from hexbytes import HexBytes

from service import client


@dataclass
class DummyAccount:
    address: str = "0x0000000000000000000000000000000000000001"


class DummyReceipt:
    def __init__(self, tx_hash: str):
        self.txn_hash = HexBytes(tx_hash)


class DummyContract:
    def __init__(self):
        self.entries = []

    def writeLog(self, verb, payload_hash, ref_id, sender):
        self.entries.append((verb, payload_hash, ref_id, sender.address))
        return DummyReceipt("0x" + "ab" * 32)

    def totalLogs(self):
        return len(self.entries)

    def getLog(self, index):
        verb, payload_hash, ref_id, actor = self.entries[index]

        class Entry:
            pass

        entry = Entry()
        entry.actor = actor
        entry.payloadHash = HexBytes(payload_hash)
        entry.verb = verb
        entry.timestamp = 1234567890 + index
        entry.refId = ref_id
        return entry


def test_submit_log_returns_tx_hash():
    contract = DummyContract()
    sender = DummyAccount()
    payload = client.LogPayload(verb="CREATE", payload_hash="0x" + "aa" * 32, ref_id="ref-123")

    tx_hash = client.submit_log(payload, sender=sender, contract=contract)

    assert tx_hash.startswith("0x")
    assert contract.entries[0][:3] == ("CREATE", "0x" + "aa" * 32, "ref-123")


def test_fetch_logs_respects_limit():
    contract = DummyContract()
    sender = DummyAccount()
    payload_hash = "0x" + "bb" * 32
    for ref in range(5):
        payload = client.LogPayload(verb="EVENT", payload_hash=payload_hash, ref_id=f"ref-{ref}")
        client.submit_log(payload, sender=sender, contract=contract)

    entries = client.fetch_logs(limit=2, contract=contract)

    assert len(entries) == 2
    assert entries[-1]["ref_id"] == "ref-4"


def test_fetch_logs_without_limit_returns_all():
    contract = DummyContract()
    sender = DummyAccount()
    payload = client.LogPayload(verb="EVENT", payload_hash="0x" + "cc" * 32, ref_id="ref")
    client.submit_log(payload, sender=sender, contract=contract)

    entries = client.fetch_logs(contract=contract)
    assert entries[0]["actor"] == sender.address


def test_submit_log_validates_hash():
    contract = DummyContract()
    sender = DummyAccount()
    payload = client.LogPayload(verb="CREATE", payload_hash="0xdeadbeef", ref_id="bad-hash")

    with pytest.raises(ValueError):
        client.submit_log(payload, sender=sender, contract=contract)
