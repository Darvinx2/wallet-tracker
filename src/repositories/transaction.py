from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Transaction
from src.schemas.transaction import TransactionCreate


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, data: TransactionCreate) -> None:
        try:
            transaction = Transaction(**data.model_dump())
            self.db.add(transaction)
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            print("Error", e)

    async def get_by_signature(self, signature: str) -> Transaction | None:
        transaction = await self.db.scalar(select(Transaction).where(Transaction.signature == signature))
        return transaction
