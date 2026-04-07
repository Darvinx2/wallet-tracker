import pytest
from fastapi import HTTPException

from app.utils.helius_auth import verify_helius_signature


class TestVerifyHeliusSignature:
    @pytest.mark.asyncio
    async def test_valid_token_passes(self, request_with_valid_token, valid_token):
        await verify_helius_signature(request_with_valid_token, valid_token)

    @pytest.mark.asyncio
    async def test_invalid_token_raises_401(self, request_with_invalid_token, valid_token):
        with pytest.raises(HTTPException) as exc_info:
            await verify_helius_signature(request_with_invalid_token, valid_token)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_empty_auth_header_raises_401(self, request_with_empty_header, valid_token):
        with pytest.raises(HTTPException) as exc_info:
            await verify_helius_signature(request_with_empty_header, valid_token)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_empty_expected_token_with_empty_header_passes(self, request_with_empty_header):
        await verify_helius_signature(request_with_empty_header, "")
