import uvicorn

from src.api.create_app import create_app
from src.core.config import get_settings


settings = get_settings()
app = create_app(settings)

if __name__ == '__main__':
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
    )
