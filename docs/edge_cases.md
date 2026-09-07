# Failure-State & Edge Case Design

The system implements explicit fail-safe handling for critical failure modes:

| Case | Scenario | Handled System Behavior |
|---|---|---|
| CASE 1 | Missing Approved Baseline | Status = `BASELINE_UNAVAILABLE`. Does NOT assume configuration is safe. Flags HIGH risk finding. |
| CASE 2 | Duplicate Config Snapshot | Deduplicates snapshots based on `(device_id, timestamp)` to prevent duplicate drift findings. |
| CASE 3 | Authorized Emergency Change | Mismatch detected but marked `AUTHORIZED` based on active approved CAB ticket. |
| CASE 4 | Unauthorized Security Weakening | Unapproved Telnet enablement elevated to `CRITICAL` severity (87+/100 risk score). |
| CASE 5 | Malformed Configuration Record | Schema validation fails gracefully; logs error in audit ledger without crashing scanner. |
| CASE 6 | Out-of-Order Timestamps | Queries latest timestamp `order_by(configuration_timestamp.desc())` ensuring valid state. |
