import pathlib
import os
import subprocess
import datetime
from argparse import ArgumentParser

CONFIG_PATH = pathlib.Path(__file__).parent.resolve() / "config.txt"
CONFIG = {}


def init_config(logs_directory, editor_command):
    logs_directory = str(pathlib.Path(logs_directory))
    file_content = [
        f"logs_directory={logs_directory}\n",
        f"editor_command={editor_command}\n",
    ]
    with open(CONFIG_PATH, "w") as cfg:
        cfg.writelines(file_content)


def read_config():
    with open(CONFIG_PATH, "r") as cfg:
        for line in cfg.readlines():
            line = line.strip()
            k, v = line.split("=")
            CONFIG[k] = v

    CONFIG["logs_directory"] = pathlib.Path(CONFIG["logs_directory"])


def ensure_today_log_exists():
    # ensure directory exists first
    os.makedirs(CONFIG["logs_directory"], exist_ok=True)

    today = datetime.date.today()
    today_log = f"{today.day}-{today.month}-{today.year % 100}.log"
    today_log_path = CONFIG["logs_directory"] / today_log
    if not os.path.isfile(today_log_path):
        with open(today_log_path, "w"):
            pass
    return today_log_path


def main():
    config_exists = os.path.isfile(CONFIG_PATH)
    parser = ArgumentParser()
    parser.add_argument(
        "--init",
        nargs=2,
        required=(not config_exists),
        metavar=("logs_directory", "editor_command"),
        help="Setup program configuration. Required as the initial command",
    )
    parser.add_argument(
        "--settings",
        help="View program configuration",
        dest="show_settings",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    if args.init is not None:
        logs_dir, editor_cmd = args.init
        init_config(logs_dir, editor_cmd)
        return

    if args.show_settings:
        with open(CONFIG_PATH, "r") as cfg:
            print(cfg.read(), end="")
        return

    read_config()

    today_log_path = ensure_today_log_exists()
    editor_command = CONFIG["editor_command"]
    subprocess.run([editor_command, today_log_path])


if __name__ == "__main__":
    main()
