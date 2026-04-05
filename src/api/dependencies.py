from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.transaction import TransactionRepository
from src.core.database import get_db


async def get_transaction_repo(
        db: AsyncSession = Depends(get_db)
):
    return TransactionRepository(db)
