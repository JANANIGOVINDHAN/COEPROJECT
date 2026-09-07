# Deployment Guide

## 1. Local Development Execution (Python + FastAPI)

```bash
# 1. Generate synthetic hospital network dataset
python data/generate_dataset.py

# 2. Train machine learning anomaly & risk models
python -m backend.ml.model_evaluation

# 3. Seed database with demo accounts, sites, rules, and baselines
python -m scripts.seed_database

# 4. Launch FastAPI Uvicorn application server
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Open web browser to: `http://localhost:8000`

## 2. Docker Deployment

```bash
# Build and run containers (PostgreSQL + FastAPI Backend)
docker compose up --build
```
Access backend API & Web UI at: `http://localhost:8000`
