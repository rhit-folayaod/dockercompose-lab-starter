"""
logging_config.py — Central logging configuration for the NBA Player Predictor API.

Provides:
- A configured root logger that writes structured lines to stdout
  (so Kubernetes / `kubectl logs` can capture them).
- A ContextVar that holds the current request's unique ID, so every
  log line emitted during a request automatically includes that ID.
"""

import logging
import sys
from contextvars import ContextVar

# Holds the current request's ID. Defaults to "-" when there is no request
# (for example, during application startup).
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    """Injects the current request_id into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configures the root logger to write to stdout with request IDs."""
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | request_id=%(request_id)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.setLevel(level)

    # Remove any default handlers so we don't double-log
    root.handlers.clear()
    root.addHandler(handler)

    return root


def get_logger(name: str) -> logging.Logger:
    """Returns a named logger (so logs show which module they came from)."""
    return logging.getLogger(name)