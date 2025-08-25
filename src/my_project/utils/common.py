from pathlib import Path
from typing import Any, List, Union
import json
import joblib
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from my_project import logger

# -------------------------
# YAML utilities
# -------------------------
# Removed ensure_annotations to avoid TypeError with ConfigBox
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with path_to_yaml.open('r', encoding='utf-8') as yaml_file:
            content = yaml.safe_load(yaml_file)
            if content is None:
                logger.warning(f"YAML file {path_to_yaml} is empty.")
                content = {}
            logger.info(f"YAML file '{path_to_yaml}' read successfully.")
            return ConfigBox(content)
    except FileNotFoundError as e:
        logger.error(f"YAML file not found: {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error reading YAML file: {e}")
        raise BoxValueError(f"Invalid YAML file: {path_to_yaml}") from e

# -------------------------
# Directory utility
# -------------------------
# Removed ensure_annotations to avoid TypeError with Union[Path, List[Path]]
def create_directories(path_to_dirs: Union[Path, List[Path]]) -> None:
    if isinstance(path_to_dirs, Path):
        path_to_dirs = [path_to_dirs]

    for path in path_to_dirs:
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created: '{path}'")
        except Exception as e:
            logger.error(f"Error creating directory '{path}': {e}")
            raise

# -------------------------
# JSON utilities
# -------------------------
@ensure_annotations
def save_json(path: Path, data: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(data, indent=4, ensure_ascii=False, default=str),
            encoding='utf-8'
        )
        logger.info(f"Data saved to JSON file: '{path}'")
    except Exception as e:
        logger.error(f"Error saving JSON file '{path}': {e}")
        raise

# Removed ensure_annotations to avoid TypeError with ConfigBox
def load_json(path: Path) -> ConfigBox:
    try:
        content = json.loads(path.read_text(encoding='utf-8'))
        logger.info(f"Data loaded from JSON file: '{path}'")
        return ConfigBox(content)
    except FileNotFoundError as e:
        logger.error(f"JSON file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {e}")
        raise ValueError(f"Invalid JSON file: {path}") from e

# -------------------------
# Binary utilities
# -------------------------
@ensure_annotations
def save_binary(path: Path, data: Any) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(data, path)
        logger.info(f"Data saved to binary file: '{path}'")
    except Exception as e:
        logger.error(f"Error saving binary file '{path}': {e}")
        raise

@ensure_annotations
def load_binary(path: Path) -> Any:
    try:
        content = joblib.load(path)
        logger.info(f"Data loaded from binary file: '{path}'")
        return content
    except FileNotFoundError as e:
        logger.error(f"Binary file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading binary file '{path}': {e}")
        raise ValueError(f"Invalid binary file: {path}") from e

# -------------------------
# File size utility
# -------------------------
@ensure_annotations
def get_size(path: Path) -> int:
    try:
        size = path.stat().st_size
        logger.info(f"Size of file '{path}': {size} bytes")
        return size
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error getting size of file '{path}': {e}")
        raise ValueError(f"Invalid file: {path}") from e
