from pydantic import BaseModel


class TransactionCreate (BaseModel):
    signature: str
    wallet_address: str | None = None
    type: str
    amount: int | None = None
    from_address: str | None = None
    to_address: str | None = None
    token_mint: str | None = None
    slot: int
    timestamp: int
    raw_data: dict
