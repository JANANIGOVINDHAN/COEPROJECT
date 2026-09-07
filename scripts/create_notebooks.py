import os
import json

notebooks_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notebooks")
os.makedirs(notebooks_dir, exist_ok=True)

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.splitlines(keepends=True)
    }

def markdown_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True)
    }

# 01 Data Exploration
nb01 = make_notebook([
    markdown_cell("# 01 - Data Exploration\nExploratory data analysis of synthetic hospital network device configurations, sites, events, and change tickets."),
    code_cell("import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\ndevices = pd.read_csv('../data/raw/devices_raw.csv')\nconfigs = pd.read_csv('../data/raw/configurations_raw.csv')\ntickets = pd.read_csv('../data/raw/change_tickets_raw.csv')\n\nprint('Raw Devices Count:', len(devices))\nprint('Raw Configurations Count:', len(configs))\nprint('Raw Change Tickets Count:', len(tickets))\ndevices.head()"),
    code_cell("configs['device_type'].value_counts().plot(kind='bar', title='Configuration Snapshots by Device Type')\nplt.show()")
])

# 02 Data Cleaning
nb02 = make_notebook([
    markdown_cell("# 02 - Data Cleaning Pipeline\nHandling missing values, duplicate snapshots, malformed VLAN strings, invalid IP addresses, and timestamp normalization."),
    code_cell("import json\nwith open('../data/cleaned/data_quality_report.json') as f:\n    quality = json.load(f)\nprint('Data Quality Summary Report:', json.dumps(quality, indent=2))"),
    code_cell("clean_configs = pd.read_csv('../data/cleaned/configurations_cleaned.csv')\nprint('Null count after cleaning:\\n', clean_configs.isnull().sum())")
])

# 03 Feature Engineering
nb03 = make_notebook([
    markdown_cell("# 03 - Feature Engineering\nExtracting numerical security score, segmentation risk metrics, and change ticket time-window alignment for ML training."),
    code_cell("ml_features = pd.read_csv('../data/processed/ml_features.csv')\nml_features.head()"),
    code_cell("ml_features['risk_label'].value_counts().plot(kind='pie', autopct='%1.1f%%', title='Target Risk Label Distribution')")
])

# 04 Baseline Analysis
nb04 = make_notebook([
    markdown_cell("# 04 - Approved Baseline Analysis\nComparing traditional field mismatch count vs proposed weighted context-aware risk engine."),
    code_cell("import json\nwith open('../docs/evaluation_metrics.json') as f:\n    metrics = json.load(f)\nprint('Proposed Engine Accuracy:', metrics.get('accuracy'))\nprint('Feature Importances:\\n', json.dumps(metrics.get('feature_importances'), indent=2))")
])

# 05 ML Anomaly Detection
nb05 = make_notebook([
    markdown_cell("# 05 - Machine Learning Anomaly Detection\nTraining Isolation Forest for unsupervised configuration pattern detection and Random Forest risk classifier."),
    code_cell("from sklearn.ensemble import IsolationForest, RandomForestClassifier\nimport pandas as pd\n\ndf = pd.read_csv('../data/processed/ml_features.csv')\nX = df[['telnet_num', 'ssh_num', 'logging_num', 'guest_iso_num', 'dhcp_snoop_num', 'security_weakening_score', 'segmentation_risk_score', 'has_authorized_ticket', 'num_changed_fields']]\n\niso = IsolationForest(contamination=0.05, random_state=42)\niso.fit(X)\nprint('Isolation forest trained on', len(X), 'samples.')")
])

# 06 Model Evaluation
nb06 = make_notebook([
    markdown_cell("# 06 - Model Evaluation & Error Analysis\nEvaluating Precision, Recall, F1-Score, Confusion Matrix, False Positives, and False Negatives."),
    code_cell("import json\nwith open('../docs/evaluation_metrics.json') as f:\n    m = json.load(f)\nprint(f'F1 Score: {m[\"f1_score\"]}')\nprint(f'Precision: {m[\"precision\"]}')\nprint(f'Recall: {m[\"recall\"]}')\nprint('Confusion Matrix:\\n', m['confusion_matrix'])")
])

files_map = {
    "01_data_exploration.ipynb": nb01,
    "02_data_cleaning.ipynb": nb02,
    "03_feature_engineering.ipynb": nb03,
    "04_baseline_analysis.ipynb": nb04,
    "05_ml_anomaly_detection.ipynb": nb05,
    "06_model_evaluation.ipynb": nb06
}

for filename, data in files_map.items():
    with open(os.path.join(notebooks_dir, filename), "w") as f:
        json.dump(data, f, indent=2)
    print(f"Created notebook {filename}")
