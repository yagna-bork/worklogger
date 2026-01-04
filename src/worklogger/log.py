import datetime
import re
import sys
import os
from enum import StrEnum

from . import config
from .util import timedelta_hours, timedelta_mins


def date_to_datetime(date):
    return datetime.datetime(date.year, date.month, date.day)


class LogEntryType(StrEnum):
    WORK = "+"
    BREAK = "="


class LogEntry:
    def __init__(self, type: LogEntryType, dt: datetime.datetime, msg: str):
        self.type = type
        self.datetime = dt
        self.msg = msg

    def __eq__(self, b):
        return self.type == b.type and self.datetime == b.datetime and self.msg == b.msg

    @staticmethod
    def entry_datetime_to_str(log_date, entry_datetime):
        """Calculate entry datetime representation for a log file

        Log files will store the time delta between the start of
        the day and the time of an entry so the user can make
        entries past midnight and into the next day without
        them reverting back to 0:00.
        """
        log_datetime = date_to_datetime(log_date)

        delta = entry_datetime - log_datetime
        delta_hours = timedelta_hours(delta)
        delta_mins = timedelta_mins(delta)
        hour_zero_padded = str(delta_hours).zfill(2)
        min_zero_padded = str(delta_mins).zfill(2)

        return f"{hour_zero_padded}:{min_zero_padded}"

    @staticmethod
    def entry_datetime_from_str(log_date, entry_time_str):
        """Convert from a str returned by `entry_datetime_to_str()` to a datetime"""
        log_datetime = date_to_datetime(log_date)
        hour_str, min_str = entry_time_str.split(":")
        delta = datetime.timedelta(hours=int(hour_str), minutes=int(min_str))
        return log_datetime + delta


class Log:
    def __init__(self, dt: datetime.date, entries: list[LogEntry] = []):
        self.date = dt
        self.entries = entries


def parse_log(log_date: datetime.date) -> Log:
    """Converts the log file for log_date into a Log object"""
    log_name = log_date.strftime(f"{config.date_format()}.log")
    log_path = config.get_setting("logs_directory") / log_name

    if not os.path.isfile(log_path):
        return Log(log_date)

    entries = []
    entry_regex = r"^([+=])([0-9][0-9]+:[0-9][0-9]) (.*)$"
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

            entry_type = LogEntryType(match.group(1))
            entry_datetime_str = match.group(2)
            entry_datetime = LogEntry.entry_datetime_from_str(
                log_date, entry_datetime_str
            )
            entry = LogEntry(entry_type, entry_datetime, msg=match.group(3))
            entries.append(entry)

    return Log(log_date, entries)
