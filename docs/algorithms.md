# Algorithms & Mathematical Formulation

## 1. Weighted Configuration Difference Score
```
difference_score = sum(w_i * diff_i) / sum(w_i)
```
Where `w_i` represents configurable field weights:
- Firewall / ACL Policy: `1.00`
- Telnet / SSH Protocol: `1.00` / `0.90`
- Client Isolation / Segmentation: `0.95`
- Syslog / Central Logging: `0.85`
- Operations (NTP / Backup): `0.70` / `0.50`

## 2. Risk Score Formulation
```
risk_score = 0.30 * S_sec + 0.20 * C_comp + 0.15 * A_auth + 0.15 * Criticality_site + 0.10 * Anomaly_ml + 0.10 * BlastRadius
```

### Risk Severity Thresholds
- **0 - 24**: LOW
- **25 - 49**: MEDIUM
- **50 - 74**: HIGH
- **75 - 100**: CRITICAL

## 3. Isolation Forest Anomaly Score
- Unsupervised Isolation Forest measures tree depth required to isolate configuration feature vectors.
- Decision function score scaled to `0 - 100`.
