
import pandas as pd

INPUT_FILE = "data/raw/transactions.csv"
OUTPUT_FILE = "data/processed/transactions_features.csv"


def build_features():
    df = pd.read_csv(INPUT_FILE)
    print("Available columns:", df.columns.tolist())
    # Parse timestamps and sort events chronologically.
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values(["user_id", "timestamp"]).reset_index(drop=True)

    # Numeric transaction amount.
    df["amount"] = pd.to_numeric(df["amount"], errors="raise")
    df["is_foreign_country"] = (df["country"] != "IN").astype(int)

    
    # Calculating rolling features separately for each user.
    results = []

    for user_id, group in df.groupby("user_id"):
        group = group.sort_values("timestamp").copy()
        group = group.set_index("timestamp")

        previous_amounts = group["amount"].shift(1)

        group["txn_count_5m"] = previous_amounts.rolling("5min").count()
        group["avg_amount_5m"] = previous_amounts.rolling("5min").mean()

        group["amount_vs_avg"] = (
            group["amount"]
            / group["avg_amount_5m"].replace(0, float("nan")))

        group["user_id"] = user_id
        results.append(group.reset_index())

    df = pd.concat(results, ignore_index=True)
   

    # Filling missing history for users' first transactions.
    df["txn_count_5m"] = df["txn_count_5m"].fillna(0)
    df["avg_amount_5m"] = df["avg_amount_5m"].fillna(0)
    df["amount_vs_avg"] = df["amount_vs_avg"].fillna(0)

    # Saving engineered features.
    df.to_csv(OUTPUT_FILE, index=False)

    print("Feature engineering completed.")
    print("Rows:", len(df))
    print("\nNew features:")
    print(df[[
        "user_id",
        "timestamp",
        "amount",
        "txn_count_5m",
        "avg_amount_5m",
        "amount_vs_avg",
        "fraud_label",
    ]].head(10))
    print("\nSaved to:", OUTPUT_FILE)


if __name__ == "__main__":
    build_features()
