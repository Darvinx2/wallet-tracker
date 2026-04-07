import pytest
from unittest.mock import AsyncMock, MagicMock

from src.services.subscription import SubscriptionService
from src.services.transaction import TransactionService
from src.services.webhook import WebhookService
from src.schemas.helius import HeliusEvent, HeliusEvents, NativeTransfer, TokenTransfers

VALID_WALLET = "11111111111111111111111111111111111111111111"
FROM_WALLET = "22222222222222222222222222222222222222222222"
TO_WALLET = "33333333333333333333333333333333333333333333"
TOKEN_MINT = "44444444444444444444444444444444444444444444"


def make_helius_event(
    native_transfers=None,
    token_transfers=None,
    signature="sig123",
    type="TRANSFER",
    slot=100,
    timestamp=1700000000,
) -> HeliusEvent:
    return HeliusEvent(
        signature=signature,
        type=type,
        timestamp=timestamp,
        nativeTransfers=native_transfers or [],
        tokenTransfers=token_transfers or [],
        events=HeliusEvents(),
        slot=slot,
    )


@pytest.fixture
def valid_wallet():
    return VALID_WALLET


@pytest.fixture
def mock_subscription_repo():
    return AsyncMock()


@pytest.fixture
def mock_transaction_repo():
    return AsyncMock()


@pytest.fixture
def mock_helius_client():
    return AsyncMock()


@pytest.fixture
def webhook_id():
    return "test-webhook-id"


@pytest.fixture
def subscription_service(mock_subscription_repo, mock_helius_client, webhook_id):
    return SubscriptionService(mock_subscription_repo, mock_helius_client, webhook_id)


@pytest.fixture
def transaction_service(mock_transaction_repo):
    return TransactionService(mock_transaction_repo)


@pytest.fixture
def webhook_service(mock_transaction_repo):
    return WebhookService(mock_transaction_repo)


@pytest.fixture
def mock_subscription(valid_wallet):
    sub = MagicMock()
    sub.wallet_address = valid_wallet
    sub.is_active = True
    return sub


@pytest.fixture
def mock_transaction():
    t = MagicMock()
    t.signature = "sig123"
    t.wallet_address = VALID_WALLET
    t.type = "TRANSFER"
    t.amount = 1000
    t.from_address = FROM_WALLET
    t.to_address = TO_WALLET
    t.token_mint = None
    t.slot = 100
    t.timestamp = 1700000000
    return t


@pytest.fixture
def native_transfer():
    return NativeTransfer(amount=1000, fromUserAccount=FROM_WALLET, toUserAccount=TO_WALLET)


@pytest.fixture
def token_transfer():
    return TokenTransfers(
        fromUserAccount=FROM_WALLET,
        toUserAccount=TO_WALLET,
        mint=TOKEN_MINT,
        tokenAmount=1.0,
    )


@pytest.fixture
def event_with_native(native_transfer):
    return make_helius_event(native_transfers=[native_transfer])


@pytest.fixture
def event_with_token(token_transfer):
    return make_helius_event(token_transfers=[token_transfer])


@pytest.fixture
def event_with_both(native_transfer, token_transfer):
    return make_helius_event(native_transfers=[native_transfer], token_transfers=[token_transfer])


@pytest.fixture
def event_with_no_transfers():
    return make_helius_event()
