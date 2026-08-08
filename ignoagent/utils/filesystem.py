"""Filesystem and path resolution utilities for IgnoAgent."""

import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Union


def get_base_path() -> Path:
    """Resolves the base directory for IgnoAgent.

    Checks IGNOAGENT_BASE_PATH environment variable, then system /opt/ignoagent,
    and falls back to project root directory in local development.

    Returns:
        Path: Base project path.
    """
    env_path = os.getenv("IGNOAGENT_BASE_PATH")
    if env_path:
        return Path(env_path)

    opt_path = Path("/opt/ignoagent")
    if opt_path.exists():
        return opt_path

    # Fallback to local repository root
    return Path(__file__).resolve().parent.parent.parent


def json_serializer(obj: Any) -> Any:
    """JSON serializer helper for data types not serializable by default.

    Args:
        obj (Any): Object to serialize.

    Returns:
        Any: Serialized value.

    Raises:
        TypeError: If object type is not supported.
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def save_json(data: Any, path: Union[str, Path], indent: int = 4) -> Path:
    """Serializes data to JSON format and saves to specified filepath.

    Args:
        data (Any): Data to serialize.
        path (Union[str, Path]): Destination file path.
        indent (int, optional): JSON indentation level. Defaults to 4.

    Returns:
        Path: The absolute path of the written file.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        file_path.parent.chmod(0o700)
    except OSError:
        pass

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, default=json_serializer, ensure_ascii=False)

    try:
        file_path.chmod(0o600)
    except OSError:
        pass

    return file_path
