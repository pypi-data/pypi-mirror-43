import io
import logging
from pathlib import Path
from typing import Optional, Union

import yaml

from .flatters import flatten_all_tasks, flatten_tasks, flatten_tests
from .naming import normalize_name, unique_name

log = logging.getLogger(__name__)


def parse_yaml_config(file_path: Path) -> Optional[dict]:
    with open(str(file_path), 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            log.warning(f"[ERR] Cannot parse yaml config file {file_path}: {exc}")
            return None


def universal_reader(input: Union['Path', 'io.TextIOBase', 'str']) -> str:
    content = input
    if isinstance(input, Path):
        content = Path(input).read_text(encoding='utf-8')
    if isinstance(input, io.TextIOBase):
        content = input.read()
    return content

