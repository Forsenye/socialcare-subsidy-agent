from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.telemetry import configure_telemetry

settings = get_settings()
configure_logging()
configure_telemetry(settings)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Simulated social subsidy orientation agent with local RAG and human handoff.",
)
app.include_router(router)
