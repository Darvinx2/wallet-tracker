from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from sqlalchemy import text

from src.core.config import Settings
from src.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

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

    @app.get("/health", include_in_schema=False)
    def health_check():
        return Response("OK")

    return app
