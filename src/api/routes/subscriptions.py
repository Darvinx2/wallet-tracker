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


@subscriptions.get("/subscriptions", response_model=list[SubscriptionResponse])
async def get_subscriptions(
        service: SubscriptionService = Depends(get_subscription_service),
) -> list[SubscriptionResponse]:
    return await service.get_all()


@subscriptions.delete("/subscriptions/{wallet_address}", status_code=204)
async def delete_subscription(
        wallet_address: str,
        service: SubscriptionService = Depends(get_subscription_service),
) -> None:
    await service.delete(wallet_address)
