"""
Logging centralizado para el sistema de marketing.
"""

import logging
import sys
from pathlib import Path
from marketing.core.config_loader import data_dir, get

_initialized = False


def setup_logging():
    global _initialized
    if _initialized:
        return
    _initialized = True

    level = getattr(logging, get("logging.level", "INFO").upper(), logging.INFO)
    fmt = get("logging.format", "%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    log_file = data_dir() / "marketing.log"

    root = logging.getLogger("marketing")
    root.setLevel(level)

    # File handler
    fh = logging.FileHandler(str(log_file), encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter(fmt))
    root.addHandler(fh)

    # Console handler (less verbose)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    root.addHandler(ch)


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(f"marketing.{name}")
