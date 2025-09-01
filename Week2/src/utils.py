import logging
import sys

def setup_logger(level=logging.INFO):
    logger = logging.getLogger("week2")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Silence external library spam
    for noisy_logger in ["httpx", "urllib3", "anyio", "h11"]:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    return logger

logger = setup_logger()