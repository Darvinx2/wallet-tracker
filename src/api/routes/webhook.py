from fastapi import APIRouter, Depends

from src.api.dependencies import get_webhook_service, verify_helius_auth
from src.schemas.helius import HeliusEvent
from src.services.webhook import WebhookService

webhook = APIRouter()


@webhook.post("/webhook/helius", dependencies=[Depends(verify_helius_auth)])
async def helius_webhook(
        payload: list[HeliusEvent],
        service: WebhookService = Depends(get_webhook_service),
) -> None:
    for event in payload:
        await service.process(event)
