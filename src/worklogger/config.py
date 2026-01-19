"""config - Module to manage the program config"""

from pathlib import Path
import sys
import os
import datetime

_CONFIG_PATH = "/usr/local/etc/worklogger.cfg"
_CONFIG = {}


# TODO call correctly
def program_name():
    return "worklogger"


# TODO call correctly
def valid_settings():
    return {"logs_directory", "editor_command"}


# TODO user should be able to configure this
def date_format():
    return "%d-%m-%y"


# TODO user should be able to configure this somehow
def time_format():
    return "%H:%M"


def deserialise_logs_directory(logs_dir: str) -> Path:
    return Path(logs_dir)


def serialise_logs_directory(logs_dir: Path):
    return str(logs_dir)


def deserialise_editor_cmd(edit_cmd: str) -> list[str]:
    return edit_cmd.split(" ")


def serialise_editor_command(edit_cmd: list[str]) -> str:
    return " ".join(edit_cmd)


def serialise_date(date: datetime.date) -> str:
    return date.strftime(date_format())


def deserialise_date(date: str) -> datetime.date:
    return datetime.date.strptime(date, date_format())


# TODO deserialise correctly
def _read_config() -> None:
    """Read config file into dictionary"""
    with open(_CONFIG_PATH, "r") as cfg:
        for line in cfg.readlines():
            line = line.strip()
            k, v = line.split("=")
            _CONFIG[k] = v

    _CONFIG["logs_directory"] = deserialise_logs_directory(_CONFIG["logs_directory"])
    _CONFIG["editor_command"] = deserialise_editor_cmd(_CONFIG["editor_command"])


def _write_config() -> None:
    """Store config dictionary into config file"""
    with open(_CONFIG_PATH, "w") as cfg:
        for k, v in _CONFIG.items():
            # serialisation
            match k:
                case "logs_directory":
                    v = serialise_logs_directory(v)
                case "editor_command":
                    v = serialise_editor_command(v)
            cfg.write(f"{k}={v}\n")


def _ensure_config() -> None:
    """Make sure config dictionary is populated before access"""
    if not _CONFIG:
        _read_config()


def get_setting(key: str):
    """Get value for key if it's valid from program configuration"""
    if key not in valid_settings():
        print("Attempted to get invalid config key: ", key, file=sys.stderr)
        return
    _ensure_config()
    return _CONFIG[key]


def set_setting(key: str, value):
    """Set value for key if it's valid in program configuration"""
    if key not in valid_settings():
        print("Attempted to set invalid config key: ", key, file=sys.stderr)
        return
    _ensure_config()
    _CONFIG[key] = value
    _write_config()


def print_config() -> None:
    with open(_CONFIG_PATH, "r") as cfg:
        print(cfg.read(), end="")


def is_config_initialised() -> bool:
    return os.path.isfile(_CONFIG_PATH)


def init_config(logs_directory: Path, editor_command: list[str]) -> None:
    _CONFIG["logs_directory"] = logs_directory
    _CONFIG["editor_command"] = editor_command
    _write_config()
