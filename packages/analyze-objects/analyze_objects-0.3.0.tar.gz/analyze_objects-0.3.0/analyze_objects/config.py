import json
import os
from typing import Tuple

import appdirs


def get_config_dir() -> str:
    """Returns the path of the configuration file."""
    return appdirs.user_config_dir("analyze_objects")


def get_find_symbols_config_path() -> str:
    """Returns the path of the configuration file for find_symbols."""
    return os.path.join(get_config_dir(), "find_symbols_config.json")


def clear_find_symbols_config() -> None:
    """Removes the find_symbols configuration file."""
    config_path = get_find_symbols_config_path()
    if os.path.isfile(config_path):
        os.remove(config_path)


def store_find_symbols_config(dumpbin_exe: str, nm_exe: str) -> None:
    """Stores the given paths in the find_symbols configuration file."""
    if dumpbin_exe and nm_exe:
        raise RuntimeError("Only one of dumpbin_exe and nm_exe may be non-empty.")
    config = dict()
    if dumpbin_exe:
        config["dumpbin_exe"] = dumpbin_exe
    elif nm_exe:
        config["nm_exe"] = nm_exe
    else:
        raise RuntimeError("One of dumpbin_exe and nm_exe must be non-empty.")
    config_path = get_find_symbols_config_path()
    config_dir = os.path.dirname(config_path)
    os.makedirs(config_dir, exist_ok=True)
    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=4)


def load_find_symbols_config() -> Tuple[str, str]:
    """Returns the tuple (dumpbin_exe, nm_exe) from the current config. No more than one path is non-empty."""
    config = dict()
    config_path = get_find_symbols_config_path()
    if os.path.isfile(config_path):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
    if "dumpbin_exe" in config and "nm_exe" in config:
        raise RuntimeError("Invalid configuration file: Only one of dumpbin_exe and nm_exe may be non-empty.")
    return config.get("dumpbin_exe", ""), config.get("nm_exe", "")
