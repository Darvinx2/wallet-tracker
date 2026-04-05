from src.clients.helius import HeliusClient
from src.repositories.subscription import SubscriptionRepository
from src.schemas.subscription import SubscriptionCreate, SubscriptionResponse


class SubscriptionService:
    def __init__(self, repo: SubscriptionRepository, helius: HeliusClient, webhook_id: str):
        self.repo = repo
        self.helius = helius
        self.webhook_id = webhook_id

    async def add(self, wallet_address: str) -> SubscriptionResponse:
        subscription = await self.repo.save(SubscriptionCreate(wallet_address=wallet_address))

        webhook = await self.helius.get_webhook(self.webhook_id)
        addresses = webhook.get("accountAddresses", [])
        if wallet_address not in addresses:
            addresses.append(wallet_address)
            await self.helius.update_webhook_addresses(self.webhook_id, addresses)

        return SubscriptionResponse(
            wallet_address=subscription.wallet_address,
            is_active=subscription.is_active,
        )
