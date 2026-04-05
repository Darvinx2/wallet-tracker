import hmac

from fastapi import Request, HTTPException


async def verify_helius_signature(request: Request, expected_token: str):
    auth_header = request.headers.get("authorization", "")

    if not hmac.compare_digest(auth_header, expected_token):
        raise HTTPException(status_code=401)
