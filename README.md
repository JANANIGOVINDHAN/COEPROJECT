# Hospital Network Configuration Drift Sentinel

> **Detecting, Explaining, Risk-Scoring, and Remediating Unauthorized Network Configuration Drift Across Distributed Hospital Campuses**

---

## 1. Project Objective

The **Hospital Network Configuration Drift Sentinel** is an enterprise network security platform designed to address critical vulnerabilities caused by unauthorized and risky network configuration drift across distributed hospital campuses (10 healthcare facilities, 113 network devices, 10,400+ snapshot records).

The system continuously compares active running configurations against approved baselines, cross-references Change Advisory Board (CAB) tickets, evaluates 31 compliance rules, trains Machine Learning anomaly detectors (Isolation Forest & Random Forest Classifier), computes composite risk scores, and generates audit evidence and CLI remediation commands.

---

## 2. Completed Components Overview

### **[PHASE 1] → Already Implemented**
- **Synthetic Data Generation Pipeline** (`data/generate_dataset.py`): Generates synthetic datasets for 10 hospital sites, 113 network devices, 10,404 config snapshots, 5,200 CAB tickets, 31 compliance rules, and 20,500 syslog events.
- **SQLite / SQLAlchemy ORM Database** (`hospital_drift.db` & `backend/models/`): Relational schema for Users, Sites, Devices, Configurations, Baselines, Findings, Tickets, Rules, and Audit Logs.
- **Core Deterministic Engines**:
  - `drift_detector.py`: Field-by-field baseline mismatch scanner.
  - `ticket_validator.py`: Cross-references change tickets against CAB window approvals.
  - `compliance_engine.py`: Evaluates configuration against 31 dynamic compliance rules.
  - `risk_engine.py`: Calculates weighted composite risk scores (0 to 100).
  - `evidence_engine.py`: Generates audit-ready evidence strings.
  - `remediation_engine.py`: Generates basic CLI fix commands.
  - `report_generator.py`: Enterprise ReportLab PDF report builder.
- **ML Foundation** (`ml_models/` & `backend/ml/`): Isolation Forest anomaly scoring model (`isolation_forest.pkl`), Random Forest risk classification model (`risk_classifier.pkl`), and feature scaler (`scaler.pkl`).
- **FastAPI REST Service** (`backend/main.py`): Core API endpoints for auth, dashboard, devices, baselines, drift findings, compliance, tickets, and reports.
- **Phase 1 Test Suite** (`tests/test_auth.py`, `test_compliance.py`, `test_devices.py`, `test_drift.py`, `test_failure_cases.py`): 12 baseline unit tests.

### **[PHASE 2] → Newly Implemented (This Task - ~35% Continuation)**
- **ML Sentinel Performance & Dynamic Retraining Engine** (`backend/api/ml_metrics.py` & `frontend/src/components/MLSentinelView.tsx`):
  - REST endpoints (`GET /api/ml/metrics`, `POST /api/ml/retrain`) for live ML metric retrieval and on-demand model retraining.
  - Interactive UI displaying Precision (100%), Recall (100%), F1-Score (100%), Confusion Matrix grid, feature importance weights, and model health state.
- **Finding Lifecycle & Remediation Management Service** (`backend/services/finding_lifecycle.py` & `backend/api/drift.py`):
  - State transitions (`OPEN`, `ACKNOWLEDGED`, `IN_PROGRESS`, `REMEDIATED`, `EXEMPTED`).
  - Interactive status update (`PATCH /drift/findings/{id}/status`) and fix execution (`POST /drift/findings/{id}/remediate`).
  - Audit log integration (`AuditLog`) tracking remediation history.
- **Historical Drift & Multi-Site Risk Analytics Service** (`backend/services/trend_analyzer.py` & `backend/api/dashboard.py`):
  - Endpoint (`GET /dashboard/trends`) delivering historical scan trends, Mean Time to Remediation (MTTR), and site vulnerability matrix.
- **Interactive Multi-Tab Single-Page Frontend SPA** (`frontend/src/App.tsx` & `frontend/src/components/`):
  - **Side-by-Side Diff Viewer Modal** (`DiffViewerModal.tsx`): Visual baseline vs live configuration diff inspector.
  - **Remediation & Evidence Console** (`RemediationConsole.tsx`): Interactive CLI fix script generator, rollback builder, and status toggle console.
  - **Compliance & Tickets Matrix** (`ComplianceTicketsView.tsx`): 31 security policies inspector and CAB ticket validator.
  - **ML Sentinel Console** (`MLSentinelView.tsx`): Real-time ML metrics dashboard.
- **Phase 2 Automated Test Suite** (`tests/test_phase2.py`): 6 comprehensive unit and integration tests covering all new Phase 2 features.

---

## 3. Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy ORM, Pydantic V2, SQLite, ReportLab
- **Machine Learning**: Scikit-Learn (Isolation Forest, Random Forest Classifier), Pandas, NumPy, Joblib
- **Frontend**: React 18, TypeScript, Tailwind CSS, Lucide React, Axios
- **Testing**: Pytest, FastAPI TestClient

---

## 4. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        React TypeScript Single-Page App                         │
│  Dashboard | Drift Findings (Diff Viewer) | Remediation | ML Sentinel | Rules   │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ REST API / JSON
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             FastAPI Web Application                             │
│ ┌───────────────────┬──────────────────────┬──────────────────────────────────┐ │
│ │ Auth & RBAC       │ Baseline Management  │ Deterministic Drift Detector     │ │
│ ├───────────────────┼──────────────────────┼──────────────────────────────────┤ │
│ │ Compliance Engine │ Ticket Validator     │ Composite Risk Engine            │ │
│ ├───────────────────┼──────────────────────┼──────────────────────────────────┤ │
│ │ Evidence Engine   │ Remediation Lifecycle│ ML Sentinel & Evaluation Router  │ │
│ └───────────────────┴──────────────────────┴──────────────────────────────────┘ │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ SQLAlchemy ORM
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SQLite Database & ML Models                           │
│   Users | Sites | Devices | Findings | Tickets | isolation_forest.pkl | RF.pkl  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Installation & Setup

### Prerequisites
- Python 3.10+ installed
- Git

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JANANIGOVINDHAN/COEPROJECT.git
   cd COEPROJECT
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database & generate synthetic data** (if running fresh):
   ```bash
   python data/generate_dataset.py
   python scripts/seed_database.py
   ```

---

## 6. How to Run the Project

### Running the Backend API
Start the FastAPI server using Uvicorn:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Once started:
- **API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Health Status Check**: `http://localhost:8000/health`
- **ML Sentinel Metrics**: `http://localhost:8000/api/ml/metrics`
- **Historical Trends**: `http://localhost:8000/dashboard/trends`

---

## 7. How to Test the Project

Run the complete test suite (Phase 1 + Phase 2 tests):
```bash
python -m pytest
```

### Test Coverage Summary
- `tests/test_auth.py`: Authentication & RBAC token issuance
- `tests/test_compliance.py`: Compliance rule evaluation
- `tests/test_devices.py`: Site & device management endpoints
- `tests/test_drift.py`: Drift scan execution & findings retrieval
- `tests/test_failure_cases.py`: Edge-cases (missing baseline, emergency tickets)
- `tests/test_phase2.py`: ML Sentinel metrics, model retraining, finding status lifecycle, remediation execution, and trend analytics

**Expected Test Output**:
```
====================== 18 passed in 6.10s ======================
```

---

## 8. Expected Outputs & Verification

- **ML Sentinel Metrics (`GET /api/ml/metrics`)**: Returns accuracy (100%), precision (100%), recall (100%), F1-score (100%), 4x4 confusion matrix, and feature importances.
- **Finding Status Update (`PATCH /drift/findings/{id}/status`)**: Transitions status and writes audit log entry.
- **Remediation Fix Execution (`POST /drift/findings/{id}/remediate`)**: Generates CLI fix commands and marks status `REMEDIATED`.
- **PDF Report Generation (`POST /reports/generate`)**: Returns downloadable audit report PDF path.

---

## 9. Current Project Completion Status

- **Phase 1**: Completed (40%)
- **Phase 2**: Completed (35%)
- **Current Completion Status**: **~75%**

---

## 10. Roadmap for Phase 3 (~25% Remaining)

- Live SSH socket integration using Netmiko/Nornir for real-time router/firewall polling.
- Webhook integrations with ServiceNow and Jira Service Management.
- Automated closed-loop remediation execution with human-in-the-loop fallback options.
