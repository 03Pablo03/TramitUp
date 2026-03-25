"""
Carga y valida la configuración central desde config.yaml.
Lee API keys de variables de entorno.
"""

import os
import yaml
from pathlib import Path
from functools import lru_cache

_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _ROOT / "config.yaml"


@lru_cache(maxsize=1)
def load_config() -> dict:
    """Carga config.yaml y lo devuelve como dict."""
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


def get(key: str, default=None):
    """Acceso dot-notation: get('brand.name') → 'TramitUp'."""
    cfg = load_config()
    parts = key.split(".")
    val = cfg
    for p in parts:
        if isinstance(val, dict) and p in val:
            val = val[p]
        else:
            return default
    return val


def get_api_key(service: str) -> str | None:
    """Lee una API key del entorno usando la config."""
    env_key = get(f"apis.{service}.env_key")
    if env_key:
        return os.environ.get(env_key)
    return None


def get_brand_color(name: str) -> str:
    """Devuelve un color de marca."""
    return get(f"brand_colors.{name}", "#1a56db")


def get_categories() -> list[dict]:
    return get("categories", [])


def get_category_ids() -> list[str]:
    return [c["id"] for c in get_categories()]


def root_dir() -> Path:
    return _ROOT


def data_dir() -> Path:
    d = _ROOT / "data"
    d.mkdir(exist_ok=True)
    return d


def output_dir() -> Path:
    d = _ROOT / "output"
    d.mkdir(exist_ok=True)
    return d
