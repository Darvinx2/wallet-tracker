from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.helius import HeliusClient
from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.repositories.subscription import SubscriptionRepository
from app.repositories.transaction import TransactionRepository
from app.services.subscription import SubscriptionService
from app.services.transaction import TransactionService
from app.services.webhook import WebhookService
from app.utils.helius_auth import verify_helius_signature


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


async def get_subscription_repo(
        db: AsyncSession = Depends(get_db)
) -> SubscriptionRepository:
    return SubscriptionRepository(db)


async def get_helius_client(
        settings: Settings = Depends(get_settings),
) -> HeliusClient:
    return HeliusClient(settings.helius_api_key)


async def get_subscription_service(
        repo: SubscriptionRepository = Depends(get_subscription_repo),
        helius: HeliusClient = Depends(get_helius_client),
        settings: Settings = Depends(get_settings),
) -> SubscriptionService:
    return SubscriptionService(repo, helius, settings.helius_webhook_id)


async def get_transaction_service(
        repo: TransactionRepository = Depends(get_transaction_repo),
) -> TransactionService:
    return TransactionService(repo)
