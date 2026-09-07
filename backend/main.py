import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

from backend.core.config import settings
from backend.core.database import engine, Base
from backend.api import auth, dashboard, devices, configurations, baselines, drift, compliance, tickets, remediation, reports, audit

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Hospital Network Configuration Drift Sentinel API - Continuous Drift Detection, Risk Scoring, Compliance, Authorization & Remediation Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(devices.router)
app.include_router(configurations.router)
app.include_router(baselines.router)
app.include_router(drift.router)
app.include_router(compliance.router)
app.include_router(tickets.router)
app.include_router(remediation.router)
app.include_router(reports.router)
app.include_router(audit.router)

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "database": "CONNECTED",
        "ml_engine": "ACTIVE"
    }

# Mount static frontend build or embedded single-page app if available
STATIC_DIR = os.path.join(settings.BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_root():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hospital Network Drift Sentinel API</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
            a { color: #38bdf8; }
            .card { background: #1e293b; padding: 24px; borderRadius: 12px; max-width: 600px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Hospital Network Configuration Drift Sentinel API</h2>
            <p>Backend API service is running successfully.</p>
            <ul>
                <li><a href="/docs">Interactive API Documentation (Swagger)</a></li>
                <li><a href="/redoc">ReDoc Documentation</a></li>
                <li><a href="/health">Health Status Check</a></li>
            </ul>
        </div>
    </body>
    </html>
    """
