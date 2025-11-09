// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title AuditLog
/// @notice Minimal append-only ledger for recording hashed audit events.
/// @dev Placeholder contract body to be implemented in subsequent iterations.
contract AuditLog {
    struct LogEntry {
        address actor;
        bytes32 payloadHash;
        string verb;
        uint256 timestamp;
        string refId;
    }

    event LogWritten(address indexed actor, bytes32 indexed payloadHash, string verb, uint256 timestamp, string refId);

    // TODO: store log entries and enforce append-only semantics.
    // function writeLog(...) external {
    // }
}
