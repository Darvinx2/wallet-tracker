from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from sqlalchemy import text

from src.api.routes.subscriptions import subscriptions
from src.api.routes.transactions import transactions
from src.api.routes.webhook import webhook
from src.clients.helius import HeliusClient
from src.clients.ngrok import get_ngrok_public_url
from src.core.config import Settings, get_settings
from src.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    settings = get_settings()
    if settings.use_ngrok:
        ngrok_url = await get_ngrok_public_url()
        webhook_url = f"{ngrok_url}/webhook/helius"
        client = HeliusClient(settings.helius_api_key)
        await client.update_webhook_url(settings.helius_webhook_id, webhook_url)
        print(f"Helius webhook updated: {webhook_url}")

    yield

    await engine.dispose()


def create_app(setting: Settings) -> FastAPI:
    app = FastAPI(
        title="Wallet Tracker API",
        description="...",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.include_router(webhook)
    app.include_router(subscriptions)
    app.include_router(transactions)

    @app.get("/health", include_in_schema=False)
    def health_check():
        return Response("OK")

    return app
