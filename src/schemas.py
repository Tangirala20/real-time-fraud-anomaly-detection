from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator
class Transaction(BaseModel):
    """Validating the incoming transaction"""
    model_config = ConfigDict(extra="forbid")
    transaction_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    amount : Decimal = Field(gt=0,max_digits=12,decimal_places=2)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    timestamp: datetime
    merchant_category: str = Field(min_length=1)
    country: str = Field(pattern=r"^[A-Z]{2}$")

    @field_validator(
        "transaction_id",
        "user_id",
        "merchant_category",)

    @classmethod
    def strip_and_validate_text(cls,value:str):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be blank")
        return value
    @field_validator("timestamp")
    @classmethod
    def required_timezone(cls,value: datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Timestamp must include timezone")
        return value

class HistoricalTransaction(Transaction):
    """Historical transaction with a known fraud label"""

    is_fraud: Literal[0,1]

