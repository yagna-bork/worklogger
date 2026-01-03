from datetime import date, datetime, time

from pathlib import Path

from src.worklogger import config
from src.worklogger.stats import (
    get_num_work_break_sessions,
    get_work_break_duration,
    get_work_sessions_desc,
)
from src.worklogger.log import parse_log

# Setup up config stub
config._CONFIG = {
    "logs_directory": Path(__file__).parent.resolve() / "test-worklogs",
    "editor_command": ["no-editor"],
}

log_date = date(2026, 1, 1)
log = parse_log(log_date)


def test_get_work_break_duration():
    expected_work_duration = {"hours": 4, "mins": 30, "total_mins": 270}
    expected_break_duration = {"hours": 1, "mins": 30, "total_mins": 90}
    work_duration, break_duration = get_work_break_duration(log)
    assert (
        work_duration == expected_work_duration
        and break_duration == expected_break_duration
    )


def test_get_num_work_break_sessions():
    nwork_sesh, nbreak_sesh = get_num_work_break_sessions(log)
    assert nwork_sesh == 4
    assert nbreak_sesh == 3


def test_get_work_break_sessions_desc():
    expected_work_sessions = [
        (
            datetime.combine(log_date, time(10, 15)),
            datetime.combine(log_date, time(11, 30)),
            {"hours": 1, "mins": 15, "total_mins": 75},
        ),
        (
            datetime.combine(log_date, time(11, 45)),
            datetime.combine(log_date, time(13)),
            {"hours": 1, "mins": 15, "total_mins": 75},
        ),
        (
            datetime.combine(log_date, time(9)),
            datetime.combine(log_date, time(10)),
            {"hours": 1, "mins": 0, "total_mins": 60},
        ),
        (
            datetime.combine(log_date, time(14)),
            datetime.combine(log_date, time(15)),
            {"hours": 1, "mins": 0, "total_mins": 60},
        ),
    ]
    expected_break_sessions = [
        (
            datetime.combine(log_date, time(13)),
            datetime.combine(log_date, time(14)),
            {"hours": 1, "mins": 0, "total_mins": 60},
        ),
        (
            datetime.combine(log_date, time(10)),
            datetime.combine(log_date, time(10, 15)),
            {"hours": 0, "mins": 15, "total_mins": 15},
        ),
        (
            datetime.combine(log_date, time(11, 30)),
            datetime.combine(log_date, time(11, 45)),
            {"hours": 0, "mins": 15, "total_mins": 15},
        ),
    ]
    work_sessions, break_sessions = get_work_sessions_desc(log)
    assert work_sessions == expected_work_sessions
    assert break_sessions == expected_break_sessions
