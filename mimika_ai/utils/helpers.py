import os
from pathlib import Path

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def get_project_root() -> Path:
    return Path(__file__).parent.parent.resolve()

def resolve_path(relative_path: str) -> str:
    return str(get_project_root() / relative_path)
