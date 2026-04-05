import httpx


class HeliusClient:
    BASE_URL = "https://api.helius.xyz/v0"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_webhook(self, webhook_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/webhooks/{webhook_id}",
                params={"api-key": self.api_key},
            )
            response.raise_for_status()
            return response.json()

    async def update_webhook_addresses(self, webhook_id: str, addresses: list[str]) -> None:
        webhook = await self.get_webhook(webhook_id)

        payload = {
            "webhookURL": webhook["webhookURL"],
            "transactionTypes": webhook["transactionTypes"],
            "accountAddresses": addresses,
            "webhookType": webhook["webhookType"],
            "authHeader": webhook.get("authHeader"),
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.BASE_URL}/webhooks/{webhook_id}",
                params={"api-key": self.api_key},
                json=payload,
            )
            if response.is_error:
                raise ValueError(f"Helius error {response.status_code}: {response.text}")

    async def update_webhook_url(self, webhook_id: str, new_url: str) -> None:
        webhook = await self.get_webhook(webhook_id)

        payload = {
            "webhookURL": new_url,
            "transactionTypes": webhook["transactionTypes"],
            "accountAddresses": webhook["accountAddresses"],
            "webhookType": webhook["webhookType"],
            "authHeader": webhook.get("authHeader"),
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.BASE_URL}/webhooks/{webhook_id}",
                params={"api-key": self.api_key},
                json=payload,
            )
            if response.is_error:
                raise ValueError(f"Helius error {response.status_code}: {response.text}")

