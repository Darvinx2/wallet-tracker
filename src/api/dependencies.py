from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.clients.helius import HeliusClient
from src.core.config import Settings, get_settings
from src.core.database import get_db
from src.repositories.subscription import SubscriptionRepository
from src.repositories.transaction import TransactionRepository
from src.services.subscription import SubscriptionService
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
