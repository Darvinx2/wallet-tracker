from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
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


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    signature: str
    wallet_address: str | None
    type: str
    amount: int | None
    from_address: str | None
    to_address: str | None
    token_mint: str | None
    slot: int
    timestamp: int
