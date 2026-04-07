import pytest

from tests.services.conftest import FROM_WALLET, TO_WALLET, TOKEN_MINT


class TestWebhookServiceProcess:
    @pytest.mark.asyncio
    async def test_process_calls_repo_save(
        self, webhook_service, mock_transaction_repo, event_with_native
    ):
        await webhook_service.process(event_with_native)

        mock_transaction_repo.save.assert_called_once()


class TestWebhookServiceGetEventInfo:
    def test_native_transfer_returns_correct_info(self, webhook_service, event_with_native):
        info = webhook_service._get_event_info(event_with_native)

        assert info["wallet_address"] == FROM_WALLET
        assert info["from_address"] == FROM_WALLET
        assert info["to_address"] == TO_WALLET
        assert info["amount"] == 1000
        assert info["token_mint"] is None

    def test_token_transfer_returns_correct_info(self, webhook_service, event_with_token):
        info = webhook_service._get_event_info(event_with_token)

        assert info["wallet_address"] == FROM_WALLET
        assert info["from_address"] == FROM_WALLET
        assert info["to_address"] == TO_WALLET
        assert info["amount"] is None
        assert info["token_mint"] == TOKEN_MINT

    def test_native_transfer_takes_priority_over_token(self, webhook_service, event_with_both):
        info = webhook_service._get_event_info(event_with_both)

        assert info["amount"] == 1000
        assert info["token_mint"] == TOKEN_MINT

    def test_no_transfers_returns_none_values(self, webhook_service, event_with_no_transfers):
        info = webhook_service._get_event_info(event_with_no_transfers)

        assert info["wallet_address"] is None
        assert info["from_address"] is None
        assert info["to_address"] is None
        assert info["amount"] is None
        assert info["token_mint"] is None


class TestWebhookServiceParseEvent:
    def test_parse_event_builds_correct_transaction(self, webhook_service, event_with_native):
        result = webhook_service._parse_event(event_with_native)

        assert result.signature == event_with_native.signature
        assert result.type == event_with_native.type
        assert result.slot == event_with_native.slot
        assert result.timestamp == event_with_native.timestamp
        assert result.from_address == FROM_WALLET
        assert result.to_address == TO_WALLET
        assert result.amount == 1000
        assert result.token_mint is None
        assert isinstance(result.raw_data, dict)

    def test_parse_event_includes_raw_data(self, webhook_service, event_with_native):
        result = webhook_service._parse_event(event_with_native)

        assert result.raw_data == event_with_native.model_dump()
