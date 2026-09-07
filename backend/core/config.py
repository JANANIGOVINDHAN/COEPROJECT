import os

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Hospital Network Configuration Drift Sentinel")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "hospital-drift-sentinel-secret-key-2026-super-secure")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
    
    # Database URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hospital_drift.db")
    
    # Risk Engine Thresholds (Configurable)
    CRITICAL_THRESHOLD: float = float(os.getenv("CRITICAL_THRESHOLD", "75.0"))
    HIGH_THRESHOLD: float = float(os.getenv("HIGH_THRESHOLD", "50.0"))
    MEDIUM_THRESHOLD: float = float(os.getenv("MEDIUM_THRESHOLD", "25.0"))
    
    # Path settings
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ML_MODEL_DIR: str = os.path.join(BASE_DIR, "ml_models")
    DATA_DIR: str = os.path.join(BASE_DIR, "data")

settings = Settings()
