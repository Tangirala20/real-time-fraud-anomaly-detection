from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.schemas import HistoricalTransaction, Transaction

def generate_transaction():
      return {
        "transaction_id": f"txn-{uuid4().hex[:8]}",
        "user_id": f"user-{uuid4().hex[:8]}",
        "amount": str(
            Decimal(str(__import__("random").randint(100, 100000) / 100))
        ),
        "currency": "INR",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "merchant_category": "electronics",
        "country": "IN",
    }
def test_valid_transaction():
    transaction = Transaction(**generate_transaction())
    assert transaction.amount > 0


def test_negative_amount_rejected():
    data = generate_transaction()
    data["amount"] = "-100"




def test_unexpected_field_rejected():
    data = generate_transaction()
    data["is_fraud"] = 1

    with pytest.raises(ValidationError):
        Transaction(**data)


def test_historical_transaction_accepts_label():
    data = generate_transaction()
    data["is_fraud"] = 1

    transaction = HistoricalTransaction(**data)
    assert transaction.is_fraud == 1
    
def test_naive_timestamp_rejected():
    data = generate_transaction()
    data["timestamp"] = datetime.now().isoformat()

    with pytest.raises(ValidationError):
        Transaction(**data)
