from fastapi import APIRouter, Depends

from app.api.dependencies import get_transaction_service
from app.schemas.transaction import TransactionResponse
from app.services.transaction import TransactionService

transactions = APIRouter()


@transactions.get("/transactions/{wallet_address}", response_model=list[TransactionResponse])
async def get_transactions(
        wallet_address: str,
        service: TransactionService = Depends(get_transaction_service),
) -> list[TransactionResponse]:
    return await service.get_by_wallet(wallet_address)
