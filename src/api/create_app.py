from fastapi import FastAPI, Response

from src.core.config import Settings


def create_app(setting: Settings) -> FastAPI:
    app = FastAPI(
        title="Wallet Tracker API",
        description="...",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/health", include_in_schema=False)
    def health_check():
        return Response("OK")

    return app
