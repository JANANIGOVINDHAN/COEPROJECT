# Hospital Network Configuration Drift Sentinel - Architecture Documentation

## System Overview
The Hospital Network Configuration Drift Sentinel is an enterprise network security platform designed to detect, explain, validate, risk-score, and suggest remediation for unauthorized configuration drift across distributed hospital campuses.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           React TypeScript Frontend SPA                         │
│   Dashboard | Sites | Devices | Baselines | Drift | Compliance | Audit | Reports │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ REST API / JWT
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             FastAPI Web Application                             │
│ ┌───────────────────┬──────────────────────┬──────────────────────────────────┐ │
│ │  Auth & RBAC      │  Baseline Management │  Deterministic Drift Comparison │ │
│ ├───────────────────┼──────────────────────┼──────────────────────────────────┤ │
│ │  Compliance Engine│  Ticket Validator    │  Risk Scoring Engine             │ │
│ ├───────────────────┼──────────────────────┼──────────────────────────────────┤ │
│ │  Evidence Engine  │  Remediation Engine  │  ML Anomaly & Risk Classifier    │ │
│ └───────────────────┴──────────────────────┴──────────────────────────────────┘ │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ SQLAlchemy ORM
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PostgreSQL / SQLite Database                             │
│   Users | Sites | Devices | Configurations | Baselines | Findings | Tickets     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Core Service Layers

1. **Authentication & RBAC**: Standardized JWT authorization with roles (`Administrator`, `Security Analyst`, `Network Engineer`).
2. **Deterministic Drift Engine**: Performs field-by-field configuration comparison against approved site/type baselines.
3. **Ticket Validator Service**: Cross-references detected drift against change request tickets in the Change Advisory Board (CAB) database.
4. **Compliance Engine**: Dynamic database-driven rule evaluator enforcing 30+ compliance policies.
5. **Risk Scoring Engine**: Weighted composite risk formula incorporating security severity, compliance status, authorization context, site criticality, ML anomaly score, and blast radius.
6. **ML Anomaly & Risk Layer**: Isolation Forest for detecting unusual configuration patterns and Random Forest for predicting risk class with confidence metrics.
7. **Evidence & Remediation Services**: Generates audit-ready evidence strings and CLI remediation commands with rollback considerations.
8. **Report Generator**: Enterprise ReportLab PDF report builder.
