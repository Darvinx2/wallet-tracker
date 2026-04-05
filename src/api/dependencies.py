from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import Settings, get_settings
from src.core.database import get_db
from src.repositories.transaction import TransactionRepository
from src.services.webhook import WebhookService
from src.utils.helius_auth import verify_helius_signature


async def get_transaction_repo(
        db: AsyncSession = Depends(get_db)
) -> TransactionRepository:
    return TransactionRepository(db)


async def get_webhook_service(
        repo: TransactionRepository = Depends(get_transaction_repo)
) -> WebhookService:
    return WebhookService(repo)


async def verify_helius_auth(
        request: Request,
        settings: Settings = Depends(get_settings),
) -> None:
    await verify_helius_signature(request, settings.helius_auth_header)
