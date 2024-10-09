import logging.config
from pathlib import Path

LOGGING_CONFIG = Path(__file__).parent / "logging.conf"


def setup_logging():
    logging.config.fileConfig(fname=LOGGING_CONFIG, disable_existing_loggers=False)
