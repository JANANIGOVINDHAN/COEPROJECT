# Methodology & Analytical Framework

## 1. Multi-Stage Detection Methodology
The Hospital Network Configuration Drift Sentinel utilizes a hybrid multi-stage detection pipeline combining deterministic rule matching with contextual metadata validation and machine learning anomaly scoring.

```
Raw Device Config -> Data Cleaning -> Baseline Match -> Field Diffs -> Ticket Validation -> Risk & ML Anomaly Scoring -> Remediation Advice
```

### Stage A: Baseline & Field-by-Field Diffing
- Deterministic comparison between active running configuration snapshots and approved site/device-type templates.
- Detects ADDED, REMOVED, MODIFIED, and MISSING configuration keys.

### Stage B: CAB Ticket Authorization Verification
- Queries Change Advisory Board (CAB) database for matching ticket IDs, device scopes, approval status, and execution windows.
- Differentiates sanctionable emergency/routine changes from unauthorized configuration drift.

### Stage C: Compliance Rule Engine
- Evaluates 30+ database-driven compliance rules (e.g. Telnet disabled, SSH v2 enforced, WPA3 enterprise, Guest Wi-Fi client isolation, syslog retention).

### Stage D: Weighted Risk & ML Anomaly Scoring
- Composite score formula:
  `risk_score = 0.30*security + 0.20*compliance + 0.15*auth + 0.15*site_criticality + 0.10*anomaly + 0.10*blast_radius`
- ML Layer: Isolation Forest for pattern anomaly detection + Random Forest classifier for risk severity prediction.
