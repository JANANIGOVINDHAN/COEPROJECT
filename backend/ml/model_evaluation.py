import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

from backend.ml.anomaly_detection import IsolationForestAnomalyDetector
from backend.ml.risk_model import RiskClassifierModel
from backend.core.config import settings

def train_and_evaluate_all():
    features_path = os.path.join(settings.DATA_DIR, "processed", "ml_features.csv")
    if not os.path.exists(features_path):
        print(f"Features file not found at {features_path}. Run generate_dataset.py first.")
        return

    df = pd.read_csv(features_path)
    
    feature_cols = [
        "telnet_num", "ssh_num", "logging_num", "guest_iso_num",
        "dhcp_snoop_num", "security_weakening_score", "segmentation_risk_score",
        "has_authorized_ticket", "num_changed_fields"
    ]
    
    X = df[feature_cols]
    y = df["risk_num"]
    
    # 1. Train Isolation Forest
    iso_detector = IsolationForestAnomalyDetector()
    iso_detector.train(X)
    
    # 2. Train Random Forest Classifier with 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    risk_classifier = RiskClassifierModel()
    risk_classifier.train(X_train, y_train)
    
    # Predict on test set
    X_test_scaled = risk_classifier.scaler.transform(X_test)
    y_pred = risk_classifier.model.predict(X_test_scaled)
    y_proba = risk_classifier.model.predict_proba(X_test_scaled)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    metrics = {
        "model_name": "Random Forest Risk Classifier",
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "confusion_matrix": cm,
        "feature_importances": {
            col: round(float(imp), 4)
            for col, imp in zip(feature_cols, risk_classifier.model.feature_importances_)
        }
    }
    
    out_dir = os.path.join(settings.BASE_DIR, "docs")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "evaluation_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
        
    print("Model Evaluation Metrics:")
    print(json.dumps(metrics, indent=2))
    return metrics

if __name__ == "__main__":
    train_and_evaluate_all()
