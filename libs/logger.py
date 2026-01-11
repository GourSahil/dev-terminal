import logging
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Regex to strip ANSI color codes (Werkzeug, Flask, etc.)
ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


class StripAnsiFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = ANSI_ESCAPE.sub("", record.msg)
        return True


def setup_logging(log_file: Path, debug: bool = False) -> None:
    """
    Configure application-wide logging.

    - Rotating file logs
    - Clean console output
    - ANSI color codes removed
    - Safe for Flask/Werkzeug
    """

    level = logging.DEBUG if debug else logging.INFO

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # ---- File handler ----
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5_000_000,   # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(StripAnsiFilter())

    # ---- Console handler ----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(StripAnsiFilter())

    # ---- Root logger ----
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Prevent duplicate handlers (Flask reloader / multiple imports)
    root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Optional: tame Werkzeug noise slightly
    logging.getLogger("werkzeug").setLevel(logging.INFO)
