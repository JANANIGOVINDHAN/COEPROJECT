import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from backend.core.config import settings

class RiskClassifierModel:
    def __init__(self):
        self.model_path = os.path.join(settings.ML_MODEL_DIR, "risk_classifier.pkl")
        self.scaler_path = os.path.join(settings.ML_MODEL_DIR, "scaler.pkl")
        self.model = None
        self.scaler = None
        self._load_or_create()

    def _load_or_create(self):
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            try:
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
            except Exception as e:
                print(f"Could not load ML risk classifier: {e}")
                self.model = None
                self.scaler = None
        if self.model is None:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.scaler = StandardScaler()

    def train(self, X: pd.DataFrame, y: pd.Series):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        os.makedirs(settings.ML_MODEL_DIR, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print("Random Forest Risk Classifier trained and saved successfully.")

    def predict_risk(self, feature_vector: list) -> tuple[str, float]:
        """
        Returns (predicted_label, confidence_score)
        """
        if self.model is None or self.scaler is None or not hasattr(self.model, "predict"):
            return "LOW", 0.85
        try:
            X_scaled = self.scaler.transform([feature_vector])
            pred_class = self.model.predict(X_scaled)[0]
            probs = self.model.predict_proba(X_scaled)[0]
            confidence = float(np.max(probs))
            
            # Map numeric class or string
            labels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            label = pred_class if isinstance(pred_class, str) else labels[min(int(pred_class), 3)]
            return label, confidence
        except Exception as e:
            print(f"Prediction fallback: {e}")
            return "LOW", 0.80
