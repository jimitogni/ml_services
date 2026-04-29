from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.api_title)
app.include_router(router)
