import pytest
from unittest.mock import MagicMock


def make_request(auth_header: str | None) -> MagicMock:
    request = MagicMock()
    request.headers.get = lambda key, default="": auth_header if key == "authorization" else default
    return request


@pytest.fixture
def valid_token():
    return "secret-token"


@pytest.fixture
def request_with_valid_token(valid_token):
    return make_request(valid_token)


@pytest.fixture
def request_with_invalid_token():
    return make_request("wrong-token")


@pytest.fixture
def request_with_missing_header():
    return make_request(None)


@pytest.fixture
def request_with_empty_header():
    return make_request("")
