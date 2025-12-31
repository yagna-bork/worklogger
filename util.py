"""util.py - Collection of functions & global variables shared between worklogger sub-modules"""

import pathlib

# Do not edit, obviously!
CONFIG_PATH = pathlib.Path(__file__).parent.resolve() / "config.txt"

_CONFIG = {}


def read_config():
    with open(CONFIG_PATH, "r") as cfg:
        for line in cfg.readlines():
            line = line.strip()
            k, v = line.split("=")
            _CONFIG[k] = v

    _CONFIG["logs_directory"] = pathlib.Path(_CONFIG["logs_directory"])
    _CONFIG["editor_command"] = _CONFIG["editor_command"].split(" ")


def config(key):
    if not _CONFIG:
        read_config()
    return _CONFIG[key]
