import logging
import sys
from .secrets import secrets


def setup_logging():
    """
    Configures logger to output to the console.
    """
    log_level = logging._nameToLevel.get(secrets.LOG_LEVEL, logging.INFO)
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
