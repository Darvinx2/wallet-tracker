from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Subscription
from src.schemas.subscription import SubscriptionCreate


class SubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, data: SubscriptionCreate) -> Subscription:
        subscription = Subscription(**data.model_dump())
        self.db.add(subscription)
        try:
            await self.db.commit()
            await self.db.refresh(subscription)
        except IntegrityError:
            await self.db.rollback()
            subscription = await self.get_by_wallet(data.wallet_address)
        return subscription

    async def get_by_wallet(self, wallet_address: str) -> Subscription | None:
        return await self.db.scalar(
            select(Subscription).where(Subscription.wallet_address == wallet_address)
        )
