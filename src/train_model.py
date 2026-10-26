
import pandas as pd
import joblib

from pathlib import Path
from xgboost import XGBClassifier
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,)

DATA_FILE = "data/processed/transactions_features.csv"
MODEL_DIR = Path("models")

FEATURES = [
    "amount",
    "txn_count_5m",
    "avg_amount_5m",
    "amount_vs_avg",
    "is_foreign_country",
]


def train_models():
    df = pd.read_csv(DATA_FILE)

    X = df[FEATURES]
    y = df["fraud_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Supervised model: XGBoost
    xgb_model = XGBClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42,
    )

    xgb_model.fit(X_train, y_train)
    xgb_predictions = xgb_model.predict(X_test)
    xgb_probabilities = xgb_model.predict_proba(X_test)[:, 1]

    print("\n=== XGBoost ===")
    print(confusion_matrix(y_test, xgb_predictions))
    print(classification_report(y_test, xgb_predictions, zero_division=0))
    print("PR-AUC:", average_precision_score(y_test, xgb_probabilities))
    print("ROC-AUC:", roc_auc_score(y_test, xgb_probabilities))

    # Unsupervised model: Isolation Forest
    # Fit only on training transactions; do not use fraud labels.
    iso_model = IsolationForest(
        n_estimators=150,
        contamination="auto",
        random_state=42,
    )

    iso_model.fit(X_train)

   # - 1 if the transaction is anamolous and 1 if its ok
    iso_predictions = (iso_model.predict(X_test) == -1).astype(int)
    iso_scores = -iso_model.decision_function(X_test)

    print("\n=== Isolation Forest ===")
    print(confusion_matrix(y_test, iso_predictions))
    print(classification_report(y_test, iso_predictions, zero_division=0))
    print("PR-AUC:", average_precision_score(y_test, iso_scores))
    print("ROC-AUC:", roc_auc_score(y_test, iso_scores))

    MODEL_DIR.mkdir(exist_ok=True)

    joblib.dump(xgb_model, MODEL_DIR / "xgboost_fraud.joblib")
    joblib.dump(iso_model, MODEL_DIR / "isolation_forest.joblib")

    print("\nBoth models saved successfully.")


if __name__ == "__main__":
    train_models()
