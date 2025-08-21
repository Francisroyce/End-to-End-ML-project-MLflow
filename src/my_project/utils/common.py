from pathlib import Path
from typing import Any, List

import json
import joblib
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from my_project import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its content as a ConfigBox object.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Returns:
        ConfigBox: Content of the YAML file as a ConfigBox object.
    """
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


@ensure_annotations(verbose=True)
def create_directories(path_to_dirs: List[Path]) -> None:
    """
    Creates directories if they do not exist.

    Args:
        path_to_dirs (List[Path]): List of directory paths to create.
    """
    for path in path_to_dirs:
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created: '{path}'")
        except Exception as e:
            logger.error(f"Error creating directory '{path}': {e}")
            raise


@ensure_annotations
def save_json(path: Path, data: Any) -> None:
    """
    Saves data to a JSON file.

    Args:
        path (Path): Path to the JSON file.
        data (Any): Data to save.
    """
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


@ensure_annotations
def load_json(path: Path) -> Any:
    """
    Loads data from a JSON file.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        Any: Content of the JSON file.
    """
    try:
        content = json.loads(path.read_text(encoding='utf-8'))
        logger.info(f"Data loaded from JSON file: '{path}'")
        return content
    except FileNotFoundError as e:
        logger.error(f"JSON file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {e}")
        raise ValueError(f"Invalid JSON file: {path}") from e


@ensure_annotations
def save_binary(path: Path, data: Any) -> None:
    """
    Saves data to a binary file using joblib.

    Args:
        path (Path): Path to the binary file.
        data (Any): Data to save.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(data, path)
        logger.info(f"Data saved to binary file: '{path}'")
    except Exception as e:
        logger.error(f"Error saving binary file '{path}': {e}")
        raise


@ensure_annotations
def load_binary(path: Path) -> Any:
    """
    Loads data from a binary file using joblib.

    Args:
        path (Path): Path to the binary file.

    Returns:
        Any: Content of the binary file.
    """
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


@ensure_annotations
def get_size(path: Path) -> int:
    """
    Gets the size of a file in bytes.

    Args:
        path (Path): Path to the file.

    Returns:
        int: Size of the file in bytes.
    """
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