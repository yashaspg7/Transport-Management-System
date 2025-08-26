import logging
import sys

from src.core.config import settings


def setup_logging():
    """Setup basic logging configuration."""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return logging.getLogger(__name__)


logger = setup_logging()
