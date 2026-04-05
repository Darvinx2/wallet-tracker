from fastapi import APIRouter, Depends

from src.api.dependencies import get_subscription_service
from src.schemas.subscription import SubscriptionCreate, SubscriptionResponse
from src.services.subscription import SubscriptionService

subscriptions = APIRouter()


@subscriptions.post("/subscriptions", response_model=SubscriptionResponse, status_code=201)
async def add_subscription(
        body: SubscriptionCreate,
        service: SubscriptionService = Depends(get_subscription_service),
) -> SubscriptionResponse:
    return await service.add(body.wallet_address)
