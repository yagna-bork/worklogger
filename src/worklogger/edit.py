import os
import subprocess
from datetime import datetime
from argparse import ArgumentParser

from . import config


def ensure_today_log_exists():
    # ensure directory exists first
    logs_directory = config.get_setting("logs_directory")
    os.makedirs(logs_directory, exist_ok=True)

    today_log = datetime.today().strftime("%d-%m-%y.log")
    today_log_path = logs_directory / today_log
    if not os.path.isfile(today_log_path):
        with open(today_log_path, "w"):
            pass
    return today_log_path


def is_last_line_empty(file_path):
    with open(file_path, "r") as file:
        sp_lines = file.read().split(os.linesep)
        return sp_lines[-1] == ""


def main(args):
    parser = ArgumentParser(prog=f"{config.PROGRAM_NAME} edit")
    parser.add_argument(
        "-n",
        "--new-entry",
        choices=["+", "="],
        help="Add an entry for current time to today's worklog with the specified type",
        dest="entry_type",
    )
    parser.add_argument(
        "-q",
        "--quit",
        dest="open_editor",
        action="store_false",
        help="Quit program before today's worklog is opened in your editor",
        default=True,
    )
    args = parser.parse_args(args)

    today_log_path = ensure_today_log_exists()

    # Begin a new entry on next line bottom of file
    # e.g. "+12:01 ..."
    # so user only has to worry about writing message
    if args.entry_type is not None:
        with open(today_log_path, "a+") as today_log:
            maybe_newline = ""
            if not is_last_line_empty(today_log_path):
                maybe_newline = "\n"
            entry_time = datetime.now().strftime("%H:%M")
            today_log.write(maybe_newline + args.entry_type + entry_time + " ")

    if args.open_editor:
        editor_command = config.get_setting("editor_command")
        subprocess.run([*editor_command, today_log_path])
