from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionResponse


class TransactionService:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    async def get_by_wallet(self, wallet_address: str) -> list[TransactionResponse]:
        transactions = await self.repo.get_by_wallet(wallet_address)
        return [TransactionResponse.model_validate(t) for t in transactions]
