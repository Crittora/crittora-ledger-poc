import pytest
from ape.exceptions import ContractLogicError
from hexbytes import HexBytes

ZERO_HASH = HexBytes("0x" + "00" * 32)
ALT_HASH = HexBytes("0x" + "11" * 32)


def test_write_log_appends_entries(project, accounts):
    deployer = accounts[0]
    actor = accounts[1]
    contract = project.AuditLog.deploy(sender=deployer)

    tx = contract.writeLog("CREATE", ZERO_HASH, "ref-1", sender=actor)
    assert tx is not None

    assert contract.totalLogs() == 1
    entry = contract.getLog(0)
    assert entry.actor == actor.address
    assert entry.payloadHash == ZERO_HASH
    assert entry.verb == "CREATE"
    assert entry.refId == "ref-1"
    assert entry.timestamp > 0


def test_get_log_out_of_range_reverts(project, accounts):
    contract = project.AuditLog.deploy(sender=accounts[0])
    contract.writeLog("UPDATE", ALT_HASH, "ref-2", sender=accounts[1])

    with pytest.raises(ContractLogicError):
        contract.getLog(2)
