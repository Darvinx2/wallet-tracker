from pydantic import BaseModel


class NativeTransfer(BaseModel):
    amount: int
    fromUserAccount: str
    toUserAccount: str


class TokenTransfers(BaseModel):
    fromUserAccount: str
    toUserAccount: str
    mint: str
    tokenAmount: float


class SwapEvent(BaseModel):
    programInfo: dict | None = None


class HeliusEvents(BaseModel):
    swap: SwapEvent | None = None


class HeliusEvent(BaseModel):
    signature: str
    type: str
    timestamp: int
    nativeTransfers: list[NativeTransfer] = []
    tokenTransfers: list[TokenTransfers] = []
    events: HeliusEvents
    slot: int


class HeliusWebhookPayload(BaseModel):
    event: list[HeliusEvent]
