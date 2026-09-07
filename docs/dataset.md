# Synthetic Dataset Specification

## Dataset Summary
All hospital site topologies, device inventory items, configuration snapshots, change request tickets, and syslog network events are synthetically generated to model a multi-campus healthcare delivery network without utilizing patient Protected Health Information (PHI) or proprietary credentials.

| Dataset Component | Total Records | File Location | Key Attributes |
|---|---|---|---|
| Hospital Sites | 10 | `data/raw/devices_raw.csv` | `site_id`, `name`, `criticality`, `code` |
| Network Devices | 113 | `data/cleaned/devices_cleaned.csv` | `device_id`, `hostname`, `type`, `zone`, `ip` |
| Config Snapshots | 10,404 | `data/cleaned/configurations_cleaned.csv` | 36 configuration parameters + timestamp |
| CAB Change Tickets | 5,200 | `data/cleaned/tickets_cleaned.csv` | `ticket_id`, `status`, `window_start`, `window_end` |
| Compliance Rules | 31 | `data/cleaned/compliance_cleaned.csv` | `rule_id`, `category`, `field`, `operator` |
| Network Events | 20,500 | `data/cleaned/network_events_cleaned.csv` | `event_id`, `event_type`, `severity`, `timestamp` |

## Data Cleaning & Quality Pipeline Metrics
- **Removed Duplicates**: 53 duplicate snapshots.
- **Fixed Malformed Values**: 6 invalid IP addresses corrected to standard subnet pools.
- **Boolean Normalization**: 12 categorical flags (`True`, `1`, `enabled`) standardized to string `"true"`/`"false"`.
- **Cleaning Success Rate**: 99.5%.
