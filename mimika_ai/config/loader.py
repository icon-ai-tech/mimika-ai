import toml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "config.toml"

def load_config():
    return toml.load(CONFIG_PATH)
