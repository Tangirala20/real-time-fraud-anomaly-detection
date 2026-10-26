
import pandas as pd
import joblib

from sklearn.metrics import (
    classification_report,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,
)

DATA_FILE = "data/processed/transactions_features.csv"
FEATURES = [
    "amount",
    "txn_count_5m",
    "avg_amount_5m",
    "amount_vs_avg",
    "is_foreign_country",
]


def validate_models():
    df = pd.read_csv(DATA_FILE)
    X = df[FEATURES]
    y = df["fraud_label"]

    print("Validation transactions:", len(df))
    print("Fraud rate:", round(y.mean(), 4))

    models = {
        "XGBoost": joblib.load("models/xgboost_fraud.joblib"),
        "Isolation Forest": joblib.load("models/isolation_forest.joblib"),
    }

    for name, model in models.items():
        if name == "XGBoost":
            predictions = model.predict(X)
            scores = model.predict_proba(X)[:, 1]
        else:
            predictions = (model.predict(X) == -1).astype(int)
            scores = -model.decision_function(X)

        print(f"\n=== {name} ===")
        print(confusion_matrix(y, predictions))
        print(classification_report(y, predictions, zero_division=0))
        print("PR-AUC:", average_precision_score(y, scores))
        print("ROC-AUC:", roc_auc_score(y, scores))


if __name__ == "__main__":
    validate_models()
