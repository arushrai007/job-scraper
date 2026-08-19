import logging
import os

LOG_FILE = "pipeline.log"

def get_logger():
    """
    Sets up a logger that writes to both the console and a log file.
    Call this once per run to get a configured logger instance.
    """
    logger = logging.getLogger("job_scraper")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if this gets called more than once
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Write logs to a file, so there's a persistent record
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Also print to console, so you see it live
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger