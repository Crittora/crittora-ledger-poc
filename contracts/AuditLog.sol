// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title AuditLog
/// @notice Minimal append-only ledger for recording hashed audit events.
/// @dev Provides append-only semantics by pushing new entries into storage and
///      emitting events for off-chain consumers.
contract AuditLog {
    struct LogEntry {
        address actor;
        bytes32 payloadHash;
        string verb;
        uint256 timestamp;
        string refId;
    }

    event LogWritten(address indexed actor, bytes32 indexed payloadHash, string verb, uint256 timestamp, string refId);

    LogEntry[] private logs;

    /// @notice Append a new audit log entry and emit a LogWritten event.
    /// @param verb Summary of the action performed.
    /// @param payloadHash Hash of the payload or document being recorded.
    /// @param refId External reference ID to correlate with off-chain records.
    /// @return entryId The index of the newly created log entry.
    function writeLog(
        string calldata verb,
        bytes32 payloadHash,
        string calldata refId
    ) external returns (uint256 entryId) {
        LogEntry memory entry = LogEntry({
            actor: msg.sender,
            payloadHash: payloadHash,
            verb: verb,
            timestamp: block.timestamp,
            refId: refId
        });

        logs.push(entry);
        emit LogWritten(entry.actor, entry.payloadHash, entry.verb, entry.timestamp, entry.refId);
        return logs.length - 1;
    }

    /// @notice Return the total number of log entries stored on-chain.
    function totalLogs() external view returns (uint256) {
        return logs.length;
    }

    /// @notice Retrieve a specific log entry by index.
    /// @dev Reverts if the index is out of bounds.
    function getLog(uint256 index) external view returns (LogEntry memory) {
        require(index < logs.length, "AuditLog:OUT_OF_RANGE");
        return logs[index];
    }
}
