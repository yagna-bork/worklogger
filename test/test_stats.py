import pathlib
import datetime

from src.worklogger import config
from src.worklogger.stats import get_log, LogEntry, LogEntryType

# Setup up config stub
config._CONFIG = {
    "logs_directory": pathlib.Path("./test-worklogs/"),
    "editor_command": ["no-editor"],
}


def test_get_log():
    # point to mock log
    date = datetime.date(2026, 1, 1)
    log = get_log(date)

    time_fmt = "%H:%M"
    expected_entries = [
        LogEntry(
            LogEntryType.WORK,
            datetime.time.strptime("9:00", time_fmt),
            "at my desk and ready to work.",
        ),
        LogEntry(
            LogEntryType.BREAK,
            datetime.time.strptime("10:00", time_fmt),
            "got through the first hour. feeling good. completed x y & z tasks.",
        ),
        LogEntry(
            LogEntryType.WORK,
            datetime.time.strptime("10:15", time_fmt),
            "went on a little stroll around the office. back at me desk.",
        ),
        LogEntry(
            LogEntryType.BREAK,
            datetime.time.strptime("11:30", time_fmt),
            "stuck on part b of task a but otherwise good progress.",
        ),
        LogEntry(
            LogEntryType.WORK,
            datetime.time.strptime("11:45", time_fmt),
            "had a nice chat with my colleague about how to complete part b of task a.",
        ),
        LogEntry(
            LogEntryType.WORK,
            datetime.time.strptime("12:30", time_fmt),
            "what my colleague said was true! i'm flying through this now.",
        ),
        LogEntry(
            LogEntryType.BREAK,
            datetime.time.strptime("13:00", time_fmt),
            msg=(
                "wow that worked great! thanks to my colleague i finally completed task a."
                "\ni'm gonna each lunch now. then finish early because i've only got a half"
                "\nday today."
            ),
        ),
        LogEntry(
            LogEntryType.WORK,
            datetime.time.strptime("14:00", time_fmt),
            "final strech of a short day. hopefully i get task c done.",
        ),
        LogEntry(
            LogEntryType.BREAK,
            datetime.time.strptime("15:00", time_fmt),
            msg=(
                "just managed to deploy task c. i'm finished for the day!"
                "\ngonna go watch the sunset and catch up on sleep."
            ),
        ),
    ]

    assert log.entries == expected_entries
