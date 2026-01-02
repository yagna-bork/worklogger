from pathlib import Path
import datetime

from src.worklogger import config
from src.worklogger.log import parse_log, LogEntry, LogEntryType

# Setup up config stub
config._CONFIG = {
    "logs_directory": Path(__file__).parent.resolve() / "test-worklogs",
    "editor_command": ["no-editor"],
}


def test_parse_log():
    # point to mock log
    log_date = datetime.date(2026, 1, 1)
    log = parse_log(log_date)

    time_fmt = "%d-%m-%y %H:%M"
    expected_entries = [
        LogEntry(
            LogEntryType.WORK,
            datetime.datetime.strptime("01-01-26 9:00", time_fmt),
            "at my desk and ready to work.",
        ),
        LogEntry(
            LogEntryType.BREAK,
            datetime.datetime.strptime("01-01-26 10:00", time_fmt),
            "got through the first hour. feeling good. completed x y & z tasks.",
        ),
        LogEntry(
            LogEntryType.WORK,
            datetime.datetime.strptime("01-01-26 10:15", time_fmt),
            "went on a little stroll around the office. back at me desk.",
        ),
        LogEntry(
            LogEntryType.BREAK,
            datetime.datetime.strptime("01-01-26 11:30", time_fmt),
            "stuck on part b of task a but otherwise good progress.",
        ),
        LogEntry(
            LogEntryType.WORK,
            datetime.datetime.strptime("01-01-26 11:45", time_fmt),
            "had a nice chat with my colleague about how to complete part b of task a.",
        ),
        LogEntry(
            LogEntryType.WORK,
            datetime.datetime.strptime("01-01-26 12:30", time_fmt),
            "what my colleague said was true! i'm flying through this now.",
        ),
        LogEntry(
            LogEntryType.BREAK,
            datetime.datetime.strptime("01-01-26 13:00", time_fmt),
            msg=(
                "wow that worked great! thanks to my colleague i finally completed task a."
                "\ni'm gonna each lunch now. then finish early because i've only got a half"
                "\nday today."
            ),
        ),
        LogEntry(
            LogEntryType.WORK,
            datetime.datetime.strptime("01-01-26 14:00", time_fmt),
            "final strech of a short day. hopefully i get task c done.",
        ),
        LogEntry(
            LogEntryType.BREAK,
            datetime.datetime.strptime("01-01-26 15:00", time_fmt),
            msg=(
                "just managed to deploy task c. i'm finished for the day!"
                "\ngonna go watch the sunset and catch up on sleep."
            ),
        ),
    ]

    assert log.entries == expected_entries
