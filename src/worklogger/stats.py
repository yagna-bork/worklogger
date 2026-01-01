import os
import re
import sys
import datetime
from argparse import ArgumentParser
from enum import Enum

from . import config


class LogEntryType(Enum):
    WORK = 1
    BREAK = 2


class LogEntry:
    def __init__(self, type, time, msg):
        self.type = type
        self.time = time
        self.msg = msg

    def __eq__(self, b):
        return self.type == b.type and self.time == b.time and self.msg == b.msg


class Log:
    def __init__(self, entries=[]):
        self.entries = entries


def get_log(date):
    log_name = date.strftime(f"{config.date_format()}.log")
    log_path = config.get_setting("logs_directory") / log_name

    if not os.path.isfile(log_path):
        return Log()

    entries = []
    entry_regex = r"^([+=])(.*?) (.*)$"
    with open(log_path, "r") as log_file:
        for lineno, line in enumerate(log_file.readlines(), start=1):
            strp_line = line.strip()

            match = re.match(entry_regex, strp_line)
            if match is None:
                if not entries:
                    print(
                        f"Skipping invalid entry {log_name}:{lineno}", file=sys.stderr
                    )
                else:
                    # this line must be continuation of previous entry's message
                    entries[-1].msg += f"\n{strp_line}"
                continue

            entry_type = (
                LogEntryType.WORK if match.group(1) == "+" else LogEntryType.BREAK
            )
            entry_time_str = match.group(2)
            entry_time = datetime.time.strptime(entry_time_str, config.time_format())

            entry = LogEntry(entry_type, entry_time, msg=match.group(3))
            entries.append(entry)

    return Log(entries)


def was_any_work_done(log):
    first_work_entry_idx = None
    for i, entry in enumerate(log.entries):
        if entry.type != LogEntryType.WORK:
            continue
        first_work_entry_idx = i
        break

    if first_work_entry_idx is None:
        return False
    if first_work_entry_idx == len(log.entries) - 1:
        return False
    return True


def get_day_start_end_length(log):
    start = log.entries[0].time
    end = log.entries[-1].time
    length = None
    return start, end, length


def print_stats_single_date(date):
    # start of day, end of day, length of day
    # total time worked, total break time, above two as percentages of day
    # work sessions desc length order
    # break sessions desc length order
    log = get_log(date)

    if not was_any_work_done(log):
        print(f"No work done on {date}")


def print_stats_date_range(from_date, to_date):
    print("Range not yet implemented.")


def main(args):
    parser = ArgumentParser(prog=f"{config.PROGRAM_NAME} stats")
    parser.add_argument(
        "dates",
        nargs="+",
        help=(
            "'dd-mm-yy' format date. If one date provided then only show stats\n"
            "for that day. Otherwise if two dates provided then show stats for\n"
            "all dates in the inclusive range bounded by both dates."
        ),
        metavar="date",
    )
    args = parser.parse_args(args)

    # check correct number of dates supplied
    num_date_args = len(args.dates)
    if num_date_args != 1 and num_date_args != 2:
        parser.print_help()
        return

    # check all dates have the correct format
    date_args = []
    for str_date in args.dates:
        try:
            date_arg = datetime.date.strptime(str_date, config.date_format())
        except ValueError:
            parser.print_help()
            return
        else:
            date_args.append(date_arg)

    if num_date_args == 1:
        print_stats_single_date(date_args[0])
    else:
        print_stats_date_range(date_args[0], date_args[1])
