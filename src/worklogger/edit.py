import os
import subprocess
import datetime
from argparse import ArgumentParser

from . import config
from .log import LogEntryType, LogEntry


def ensure_today_log_exists() -> str:
    """Get path for today's log and create it if it doesn't exist"""
    # ensure the logs directory exists first
    logs_dir = config.get_setting("logs_directory")
    os.makedirs(logs_dir, exist_ok=True)

    today_str = config.serialise_date(datetime.date.today())
    path = logs_dir / f"{today_str}.log"
    if not os.path.isfile(path):
        with open(path, "w"):
            pass
    return path


def is_last_line_non_empty(file_path):
    with open(file_path, "r") as file:
        sp_lines = file.read().split(os.linesep)
        return sp_lines[-1] != ""


def main(args):
    today = datetime.date.today()

    parser = ArgumentParser(prog=f"{config.program_name()} edit")
    parser.add_argument(
        "-n",
        "--new",
        choices=["+", "="],
        type=LogEntryType,
        help="Add entry for current time to worklog with the specified type",
        dest="entry_type",
    )
    parser.add_argument(
        "-q",
        "--quit",
        dest="open_editor",
        action="store_false",
        help="Quit program before worklog is opened in your editor",
        default=True,
    )
    parser.add_argument(
        "-d",
        "--date",
        type=config.deserialise_date,
        help=(
            "The dd-mm-yy formated date for the log that this program should use. "
            "The log must already have been created. Default: today"
        ),
        dest="log_date",
        default=today,
    )
    args = parser.parse_args(args)

    log_path = ""
    if args.log_date != today:
        # check log exists for that date
        log_name = f"{config.serialise_date(args.log_date)}.log"
        log_path = config.get_setting("logs_directory") / log_name
        if not os.path.isfile(log_path):
            parser.print_help()
            return
    else:
        log_path = ensure_today_log_exists()

    # Begin a new entry on new line at bottom of file
    # e.g. "+12:01 ..."
    # so user only has to worry the message
    if args.entry_type is not None:
        maybe_newline = "\n" if is_last_line_non_empty(log_path) else ""
        with open(log_path, "a+") as log_file:
            entry_type = str(args.entry_type)
            now = datetime.datetime.now()
            entry_datetime = LogEntry.entry_datetime_str(args.log_date, now)
            log_file.write(f"{maybe_newline}{entry_type}{entry_datetime} ")

    if args.open_editor:
        edit_cmd = config.get_setting("editor_command")
        subprocess.run([*edit_cmd, log_path])
