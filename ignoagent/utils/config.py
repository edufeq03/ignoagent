"""Configuration loading functions for IgnoAgent."""

from datetime import date
from typing import Any, Dict
import yaml

from ignoagent.utils.filesystem import get_base_path


import os

def load_config() -> Dict[str, Any]:
    """Loads application configuration from config/config.yml or environment variables.

    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    config_file = get_base_path() / "config" / "config.yml"
    data = {}
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    # Environment variable overrides (Segurança & Doze Fatores)
    if "api" not in data:
        data["api"] = {}

    if os.getenv("IGNOAGENT_API_TOKEN"):
        data["api"]["token"] = os.getenv("IGNOAGENT_API_TOKEN")

    if os.getenv("IGNOAGENT_API_URL"):
        data["api"]["url"] = os.getenv("IGNOAGENT_API_URL")

    return data


def load_identity() -> Dict[str, Any]:
    """Loads agent identity configuration from config/identity.yml.

    Returns:
        Dict[str, Any]: Identity metadata dictionary.
    """
    identity_file = get_base_path() / "config" / "identity.yml"
    if not identity_file.exists():
        return {}

    with open(identity_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.isoformat()

    return data


def load_collector_config() -> Dict[str, Any]:
    """Loads collectors specific configurations.

    Returns:
        Dict[str, Any]: Collectors configuration section.
    """
    config = load_config()
    return config.get("collectors", {})


def load_reports_config() -> Dict[str, Any]:
    """Loads reports output configuration.

    Returns:
        Dict[str, Any]: Reports configuration section.
    """
    config = load_config()
    return config.get("reports", {})
