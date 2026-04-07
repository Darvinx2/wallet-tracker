import pytest
from fastapi import HTTPException

from app.schemas.subscription import SubscriptionResponse


class TestSubscriptionServiceAdd:
    @pytest.mark.asyncio
    async def test_add_saves_subscription_and_updates_helius(
        self, subscription_service, mock_subscription_repo, mock_helius_client, mock_subscription, valid_wallet, webhook_id
    ):
        mock_subscription_repo.save.return_value = mock_subscription
        mock_helius_client.get_webhook.return_value = {"accountAddresses": []}

        result = await subscription_service.add(valid_wallet)

        mock_subscription_repo.save.assert_called_once()
        mock_helius_client.update_webhook_addresses.assert_called_once_with(webhook_id, [valid_wallet])
        assert isinstance(result, SubscriptionResponse)
        assert result.wallet_address == valid_wallet
        assert result.is_active is True

    @pytest.mark.asyncio
    async def test_add_does_not_update_helius_if_wallet_already_tracked(
        self, subscription_service, mock_subscription_repo, mock_helius_client, mock_subscription, valid_wallet
    ):
        mock_subscription_repo.save.return_value = mock_subscription
        mock_helius_client.get_webhook.return_value = {"accountAddresses": [valid_wallet]}

        await subscription_service.add(valid_wallet)

        mock_helius_client.update_webhook_addresses.assert_not_called()


class TestSubscriptionServiceGetAll:
    @pytest.mark.asyncio
    async def test_get_all_returns_list(
        self, subscription_service, mock_subscription_repo, mock_subscription
    ):
        mock_subscription_repo.get_all.return_value = [mock_subscription, mock_subscription]

        result = await subscription_service.get_all()

        assert len(result) == 2
        assert all(isinstance(r, SubscriptionResponse) for r in result)

    @pytest.mark.asyncio
    async def test_get_all_returns_empty_list(
        self, subscription_service, mock_subscription_repo
    ):
        mock_subscription_repo.get_all.return_value = []

        result = await subscription_service.get_all()

        assert result == []


class TestSubscriptionServiceDelete:
    @pytest.mark.asyncio
    async def test_delete_removes_and_updates_helius(
        self, subscription_service, mock_subscription_repo, mock_helius_client, valid_wallet, webhook_id
    ):
        mock_subscription_repo.delete.return_value = True
        mock_helius_client.get_webhook.return_value = {"accountAddresses": [valid_wallet]}

        await subscription_service.delete(valid_wallet)

        mock_subscription_repo.delete.assert_called_once_with(valid_wallet)
        mock_helius_client.update_webhook_addresses.assert_called_once_with(webhook_id, [])

    @pytest.mark.asyncio
    async def test_delete_does_not_update_helius_if_wallet_not_tracked(
        self, subscription_service, mock_subscription_repo, mock_helius_client, valid_wallet
    ):
        mock_subscription_repo.delete.return_value = True
        mock_helius_client.get_webhook.return_value = {"accountAddresses": []}

        await subscription_service.delete(valid_wallet)

        mock_helius_client.update_webhook_addresses.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_raises_404_if_not_found(
        self, subscription_service, mock_subscription_repo, valid_wallet
    ):
        mock_subscription_repo.delete.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            await subscription_service.delete(valid_wallet)

        assert exc_info.value.status_code == 404
