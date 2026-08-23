"""Small logging helper used by application services."""

import logging
import os


def configure_logging() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/gethired.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    return logging.getLogger("GetHired")
