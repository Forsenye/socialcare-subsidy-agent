import logging

from app.core.config import Settings

logger = logging.getLogger(__name__)


def configure_telemetry(settings: Settings) -> None:
    """Placeholder for Application Insights/OpenTelemetry setup."""
    if settings.appinsights_connection_string:
        logger.info("Application Insights connection string detected; telemetry can be enabled.")
    else:
        logger.info("Application Insights is not configured; using local structured logs.")
