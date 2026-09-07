import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from backend.core.config import settings

class IsolationForestAnomalyDetector:
    def __init__(self):
        self.model_path = os.path.join(settings.ML_MODEL_DIR, "isolation_forest.pkl")
        self.model = None
        self._load_or_create()

    def _load_or_create(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"Could not load Isolation Forest model: {e}")
                self.model = None
        if self.model is None:
            self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

    def train(self, X: pd.DataFrame):
        self.model.fit(X)
        os.makedirs(settings.ML_MODEL_DIR, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Isolation Forest model trained and saved to {self.model_path}")

    def predict_anomaly(self, feature_vector: list) -> float:
        """
        Returns an anomaly score scaled between 0 and 100.
        Higher score = more anomalous.
        """
        if self.model is None or not hasattr(self.model, "decision_function"):
            return 25.0
        try:
            # decision_function returns negative values for anomalies
            df_val = self.model.decision_function([feature_vector])[0]
            # Convert decision function score to 0 - 100
            anomaly_score = max(0.0, min(100.0, (0.5 - df_val) * 100.0))
            return float(anomaly_score)
        except Exception:
            return 25.0
