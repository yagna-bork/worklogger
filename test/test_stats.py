import datetime

from pathlib import Path

from src.worklogger import config
from src.worklogger.stats import get_work_break_duration
from src.worklogger.log import parse_log

# Setup up config stub
config._CONFIG = {
    "logs_directory": Path(__file__).parent.resolve() / "test-worklogs",
    "editor_command": ["no-editor"],
}


def test_get_work_break_duration():
    log_date = datetime.date(2026, 1, 1)
    log = parse_log(log_date)

    expected_work_duration = {"hours": 4, "mins": 30, "total_mins": 270}
    expected_break_duration = {"hours": 1, "mins": 30, "total_mins": 90}
    work_duration, break_duration = get_work_break_duration(log)
    assert (
        work_duration == expected_work_duration
        and break_duration == expected_break_duration
    )
