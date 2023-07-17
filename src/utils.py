import os
import yaml
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError

from src.logger import logging

def read_yaml(path: Path) -> ConfigBox:
    """Read `yaml` file and return a ConfigBox object.
    Args:
        path: Path for yaml config file.
    Returns:
        ConfigBox: ConfigBox object representing the content of the YAML file.
    """
    try:
        with open(path) as yaml_fp:
            content = yaml.safe_load(yaml_fp)
            logging.info(f"Yaml Config file successfully loaded from path: {path}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as err:
        raise err

def get_size(path: Path) -> float:
    """Get size of file in KB.
    Args:
        path: Path of the file.
    Returns:
        size (float): Size of the file in KB.
    """
    size_in_kb = round(os.path.getsize(path) / 1024, 2)
    return size_in_kb
