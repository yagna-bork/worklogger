"""config.py - Module to manage the program config"""

import pathlib
import sys
import os

_CONFIG_PATH = pathlib.Path(__file__).parent.resolve() / "config.txt"
_CONFIG = {}

VALID_SETTINGS = ["logs_directory", "editor_command"]


def _read_config():
    """Read config file into dictionary"""
    with open(_CONFIG_PATH, "r") as cfg:
        for line in cfg.readlines():
            line = line.strip()
            k, v = line.split("=")
            _CONFIG[k] = v

    _CONFIG["logs_directory"] = pathlib.Path(_CONFIG["logs_directory"])
    _CONFIG["editor_command"] = _CONFIG["editor_command"].split(" ")


def _write_config():
    """Store config dictionary into config file"""
    with open(_CONFIG_PATH, "w") as cfg:
        for k, v in _CONFIG.items():
            # note: we don't serialise values because this
            # function is only called by set_config and
            # init_config which already set values
            # to raw inputs from user
            cfg.write(f"{k}={v}\n")


def _ensure_config():
    if not _CONFIG:
        _read_config()


def config(key):
    _ensure_config()
    return _CONFIG[key]


def set_config(key, value):
    if key not in VALID_SETTINGS:
        print("Attempted to set invalid config key: ", key, file=sys.stderr)

    _ensure_config()
    _CONFIG[key] = value
    _write_config()
    _read_config()


def print_config():
    with open(_CONFIG_PATH, "r") as cfg:
        print(cfg.read(), end="")


def is_config_initialised():
    return os.path.isfile(_CONFIG_PATH)


def init_config(logs_directory, editor_command):
    _CONFIG["logs_directory"] = logs_directory
    _CONFIG["editor_command"] = editor_command
    _write_config()
