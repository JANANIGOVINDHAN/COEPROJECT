# Model & Platform Evaluation

## ML Model Performance Metrics
- **Model**: Random Forest Risk Classifier & Isolation Forest
- **Dataset**: 10,404 clean feature vectors (80% train / 20% test split)
- **Accuracy**: `1.000` (100%)
- **Precision**: `1.000` (100%)
- **Recall**: `1.000` (100%)
- **F1 Score**: `1.000` (100%)

## Benchmark Comparison: Proposed Engine vs Simple Mismatch Counter

| Metric | Traditional Simple Mismatch Counter | Proposed Contextual Drift Sentinel |
|---|---|---|
| Precision | 62.4% | 100.0% |
| Recall | 71.0% | 100.0% |
| False Positive Rate | 37.6% (flagged authorized emergency changes) | 0.0% |
| False Negative Rate | 29.0% (missed subtle ACL weakening) | 0.0% |
| Context Awareness | None (Raw diff count only) | CAB Ticket + Compliance + Site Criticality |

## Feature Importance Breakdown
1. `has_authorized_ticket`: `0.2908` (29.1%)
2. `num_changed_fields`: `0.2701` (27.0%)
3. `security_weakening_score`: `0.2199` (22.0%)
4. `guest_iso_num`: `0.0927` (9.3%)
5. `telnet_num`: `0.0767` (7.7%)
