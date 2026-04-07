from fastapi import APIRouter, Depends

from app.api.dependencies import get_webhook_service, verify_helius_auth
from app.schemas.helius import HeliusEvent
from app.services.webhook import WebhookService

webhook = APIRouter()


@webhook.post("/webhook/helius", dependencies=[Depends(verify_helius_auth)])
async def helius_webhook(
        payload: list[HeliusEvent],
        service: WebhookService = Depends(get_webhook_service),
) -> None:
    for event in payload:
        await service.process(event)
