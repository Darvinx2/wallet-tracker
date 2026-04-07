import re

from pydantic import BaseModel, field_validator

SOLANA_ADDRESS_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{44}$")


class SubscriptionCreate(BaseModel):
    wallet_address: str

    @field_validator("wallet_address")
    @classmethod
    def validate_solana_address(cls, v: str) -> str:
        if not SOLANA_ADDRESS_RE.match(v):
            raise ValueError("Invalid Solana address")
        return v


class SubscriptionResponse(BaseModel):
    wallet_address: str
    is_active: bool
