import pytest

from src.schemas.transaction import TransactionResponse


class TestTransactionServiceGetByWallet:
    @pytest.mark.asyncio
    async def test_get_by_wallet_returns_list(
        self, transaction_service, mock_transaction_repo, mock_transaction, valid_wallet
    ):
        mock_transaction_repo.get_by_wallet.return_value = [mock_transaction]

        result = await transaction_service.get_by_wallet(valid_wallet)

        mock_transaction_repo.get_by_wallet.assert_called_once_with(valid_wallet)
        assert len(result) == 1
        assert all(isinstance(r, TransactionResponse) for r in result)

    @pytest.mark.asyncio
    async def test_get_by_wallet_returns_empty_list(
        self, transaction_service, mock_transaction_repo, valid_wallet
    ):
        mock_transaction_repo.get_by_wallet.return_value = []

        result = await transaction_service.get_by_wallet(valid_wallet)

        assert result == []
