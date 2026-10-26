
import csv
from pathlib import Path
import random
import time
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from pydantic import ValidationError

from src.schemas import Transaction

OUTPUT_FILE = Path("data/raw/transactions.csv")

USERS = [f"user-{i:03d}" for i in range(1, 101)]
MERCHANT_CATEGORIES = [
    "groceries", "electronics", "travel", "restaurants", "fuel"
]
COUNTRIES = ["IN", "IN", "UK", "US", "GB"]

# Simulated user profiles: most users normally transact in India.
USER_HOME_COUNTRY = {user: "IN" for user in USERS}
def generate_transaction() -> dict:
    """Generate a simulated transaction and a training label."""
    user_id = random.choice(USERS)
    is_suspicious = random.random() < 0.10

    amount = random.randint(100, 20000) / 100
    country = USER_HOME_COUNTRY[user_id]

    if is_suspicious:
        pattern = random.choice(["high_amount", "unusual_country"])

        if pattern == "high_amount":
            amount = random.randint(50000, 200000) / 100
        else:
            country = random.choice(["US", "GB"])

    return {
        "transaction_id": f"txn-{uuid4().hex[:12]}",
        "user_id": user_id,
        "amount": str(Decimal(str(round(amount, 2)))),
        "currency": "INR",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "merchant_category": random.choice(MERCHANT_CATEGORIES),
        "country": country,
        "is_suspicious": is_suspicious,
        "fraud_label": int(is_suspicious),
    }

def stream_transactions(
    interval_seconds: float = 0.1,
    max_transactions: int = 5000,
) -> None:
    """Generate, validate, and save transactions to CSV."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "transaction_id",
        "user_id",
        "amount",
        "currency",
        "timestamp",
        "merchant_category",
        "country",
        "is_suspicious",
        "fraud_label",
    ]

    generated = 0
    rejected = 0

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        try:
            while generated < max_transactions:
                event = generate_transaction()

                is_suspicious = event.pop("is_suspicious")
                fraud_label = event.pop("fraud_label")

                try:
                    transaction = Transaction(**event)

                    row = transaction.model_dump(mode="json")
                    row["is_suspicious"] = is_suspicious
                    row["fraud_label"] = fraud_label

                    writer.writerow(row)
                    file.flush()

                    generated += 1

                    print(
                        f"{generated}/{max_transactions} | "
                        f"SUSPICIOUS={is_suspicious} | "
                        f"LABEL={fraud_label} | "
                        f"AMOUNT={transaction.amount} INR"
                    )

                except ValidationError as exc:
                    rejected += 1
                    print(f"REJECTED: {exc}")

                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            print("\nGeneration interrupted by user.")

    print(f"\nGenerated: {generated}")
    print(f"Rejected: {rejected}")
    print(f"Saved dataset: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    stream_transactions(max_transactions=5000)
