import logging
import sys
from .secrets import secrets


def setup_logging():
    """
    Configures a simple, clean logger to output to the console.
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    log_level = logging._nameToLevel.get(secrets.LOG_LEVEL, logging.INFO)

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    logging.info("Logging configured successfully.")
