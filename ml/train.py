"""
train.py — Flash Flood Risk Model Training

Trains a Random Forest classifier to predict flood_occurred (0/1) using
rainfall, terrain, soil moisture, and river level features. Also trains
the model to work as a probability-based risk score (0-100) for the
dashboard map.

Run: python train.py
Output: model/flood_rf_model.joblib, model/land_use_encoder.joblib
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_recall_curve,
)
import joblib
import os

DATA_PATH = "data/sih_flash_flood_dataset.csv"
MODEL_DIR = "model"

FEATURE_COLUMNS = [
    "rainfall_mm_3h",
    "rainfall_mm_24h",
    "slope_deg",
    "soil_moisture",
    "river_level_m",
    "land_use_encoded",
]
TARGET_COLUMN = "flood_occurred"


def load_and_prepare_data(path):
    df = pd.read_csv(path)

    # Encode categorical land_use_type -> numeric
    le = LabelEncoder()
    df["land_use_encoded"] = le.fit_transform(df["land_use_type"])

    return df, le


def train_model(df):
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # class_weight='balanced' handles the heavy imbalance
    # (only ~0.7% of rows are actual flood events)
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # --- Evaluation ---
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("=" * 50)
    print("Classification report (test set):")
    print(classification_report(y_test, y_pred, digits=3))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}")
    print("=" * 50)

    # Feature importance — useful for the pitch deck
    importances = pd.Series(model.feature_importances_, index=FEATURE_COLUMNS)
    print("Feature importances:")
    print(importances.sort_values(ascending=False))

    return model, (X_test, y_test, y_proba)


def find_best_threshold(y_test, y_proba):
    """
    Default 0.5 threshold is a bad idea for imbalanced data.
    This finds a threshold that favors recall (catching real floods)
    without flooding (pun intended) the dashboard with false alarms.
    """
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
    # pick threshold with recall >= 0.8 and best precision at that recall
    best_idx = None
    for i, r in enumerate(recalls):
        if r >= 0.8:
            best_idx = i
    if best_idx is not None and best_idx < len(thresholds):
        return thresholds[best_idx]
    return 0.5


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    df, land_use_encoder = load_and_prepare_data(DATA_PATH)
    model, (X_test, y_test, y_proba) = train_model(df)

    best_threshold = find_best_threshold(y_test, y_proba)
    print(f"\nRecommended decision threshold: {best_threshold:.3f}")

    joblib.dump(model, os.path.join(MODEL_DIR, "flood_rf_model.joblib"))
    joblib.dump(land_use_encoder, os.path.join(MODEL_DIR, "land_use_encoder.joblib"))
    joblib.dump(best_threshold, os.path.join(MODEL_DIR, "decision_threshold.joblib"))

    print(f"\nSaved model + encoder + threshold to '{MODEL_DIR}/'")


if __name__ == "__main__":
    main()
