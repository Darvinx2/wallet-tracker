import logging

from app.repositories.transaction import TransactionRepository
from app.schemas.helius import HeliusEvent
from app.schemas.transaction import TransactionCreate

logger = logging.getLogger(__name__)


class WebhookService:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    async def process(self, event: HeliusEvent) -> None:
        logger.info("Processing event signature=%s type=%s", event.signature, event.type)
        data = self._parse_event(event)
        await self.repo.save(data)

    @staticmethod
    def _get_event_info(event: HeliusEvent) -> dict:
        native = event.nativeTransfers
        token = event.tokenTransfers
        transfer = native[0] if native else token[0] if token else None

        return {
            "wallet_address": transfer.fromUserAccount if transfer else None,
            "amount": native[0].amount if native else None,
            "from_address": transfer.fromUserAccount if transfer else None,
            "to_address": transfer.toUserAccount if transfer else None,
            "token_mint": token[0].mint if token else None,
        }

    def _parse_event(self, event: HeliusEvent) -> TransactionCreate:
        info = self._get_event_info(event)
        return TransactionCreate(
            signature=event.signature,
            type=event.type,
            slot=event.slot,
            timestamp=event.timestamp,
            raw_data=event.model_dump(),
            **info,
        )
