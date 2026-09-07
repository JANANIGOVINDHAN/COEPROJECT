# Ethics, Safety & Responsible AI Note

## Ethical & Safety Commitments

1. **Zero Patient PHI**: No real patient health records, names, or clinical data are stored or processed. All datasets are 100% synthetic.
2. **No Automatic Live Network Mutation**: The Sentinel is strictly a **detection and recommendation** prototype. It generates CLI commands for human review but NEVER executes write operations directly on live hospital routers or firewalls without human approval.
3. **Auditability & Transparency**: Every configuration scan, baseline update, rule modification, and user action is logged in an immutable audit ledger (`AuditLog`).
4. **Explainable AI (XAI)**: Machine learning predictions (Isolation Forest & Random Forest) provide component risk breakdowns and feature importances. ML outputs are never treated as absolute truth; deterministic field diffing remains the primary authority.
5. **No Production Credentials**: All passwords and secrets are configurable via environment variables, with safe demo credentials provided for local testing only.
