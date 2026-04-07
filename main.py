import uvicorn

from app.api.create_app import create_app
from app.core.config import get_settings


settings = get_settings()
app = create_app(settings)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
    )
