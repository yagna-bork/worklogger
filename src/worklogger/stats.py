from argparse import ArgumentParser
from typing import TypedDict, Tuple, NamedTuple
import datetime

from . import config
from .log import parse_log, LogEntryType, Log
from .util import timedelta_hours, timedelta_mins


class Duration(TypedDict):
    hours: int
    mins: int
    total_mins: int


class Session(NamedTuple):
    start: datetime.datetime
    end: datetime.datetime
    duration: Duration


def was_work_done(log: Log) -> bool:
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


def get_day_start_end_duration(
    log: Log,
) -> Tuple[datetime.datetime, datetime.datetime, Duration]:
    start = log.entries[0].datetime
    end = log.entries[-1].datetime
    delta = end - start
    duration: Duration = {
        "hours": timedelta_hours(delta),
        "mins": timedelta_mins(delta),
        "total_mins": delta.seconds // 60,
    }
    return start, end, duration


def get_work_break_duration(log: Log) -> Tuple[Duration, Duration]:
    time_worked = datetime.timedelta()
    time_breaked = datetime.timedelta()
    curr_type = log.entries[0].type
    curr_time = log.entries[0].datetime
    for entry in log.entries[1:]:
        if entry.type == curr_type:
            continue
        if curr_type == LogEntryType.WORK:
            time_worked += entry.datetime - curr_time
        else:
            time_breaked += entry.datetime - curr_time
        curr_type = entry.type
        curr_time = entry.datetime

    work_duration: Duration = {
        "hours": timedelta_hours(time_worked),
        "mins": timedelta_mins(time_worked),
        "total_mins": time_worked.seconds // 60,
    }
    break_duration: Duration = {
        "hours": timedelta_hours(time_breaked),
        "mins": timedelta_mins(time_breaked),
        "total_mins": time_breaked.seconds // 60,
    }
    return work_duration, break_duration


def get_num_work_break_sessions(log: Log) -> Tuple[int, int]:
    num_work_sessions = num_break_sessions = 0
    curr_type = log.entries[0].type
    for entry in log.entries[1:]:
        # we count multiple contiguous entries of
        # the same type as a single session
        if entry.type == curr_type:
            continue
        if curr_type == LogEntryType.WORK:
            num_work_sessions += 1
        else:
            num_break_sessions += 1
        curr_type = entry.type
    return num_work_sessions, num_break_sessions


def get_work_break_sessions_desc(
    log: Log,
) -> Tuple[list[Session], list[Session]]:
    work_sessions: list[Session] = []
    break_sessions: list[Session] = []

    curr_type = log.entries[0].type
    curr_time = log.entries[0].datetime
    for entry in log.entries[1:]:
        if entry.type == curr_type:
            continue

        start = curr_time
        end = entry.datetime
        delta = end - start
        duration: Duration = {
            "hours": timedelta_hours(delta),
            "mins": timedelta_mins(delta),
            "total_mins": delta.seconds // 60,
        }
        session = Session(start, end, duration)

        if entry.type == LogEntryType.BREAK:
            # going from WORK -> BREAK so ending a WORK session
            work_sessions.append(session)
        else:
            # going from BREAK -> WORK so ending a BREAK session
            break_sessions.append(session)
        curr_type = entry.type
        curr_time = entry.datetime

    work_sessions.sort(key=lambda sesh: sesh.duration["total_mins"], reverse=True)
    break_sessions.sort(key=lambda sesh: sesh.duration["total_mins"], reverse=True)
    return work_sessions, break_sessions


def duration_to_str(duration: Duration, label: str) -> str:
    return f"{label}: {duration['hours']} hours, {duration['mins']} minutes"


def datetime_to_str(log_date: datetime.date, dt: datetime.datetime) -> str:
    """Str representation with date component if it's different to date of the log"""
    st = ""
    date, time = dt.date(), dt.time()
    if date != log_date:
        st += f"{date.strftime(config.date_format())} "
    st += time.strftime(config.time_format())
    return st


def print_stats_single_date(date: datetime.date) -> None:
    log = parse_log(date)

    date_str = config.serialise_date(date)
    print(date_str)
    print("-" * len(date_str))

    if not was_work_done(log):
        print(f"No work done on {date_str}")
        return

    # Start of day, end of day, length of day
    start, end, duration = get_day_start_end_duration(log)
    print("Started:", datetime_to_str(date, start))
    print("Ended:", datetime_to_str(date, end))
    print(duration_to_str(duration, "Duration"))
    print()

    # Total time worked, total break time, both as percentages of entire day
    work_duration, break_duration = get_work_break_duration(log)

    work_pct = work_duration["total_mins"] / duration["total_mins"] * 100
    break_pct = break_duration["total_mins"] / duration["total_mins"] * 100
    work_pct, break_pct = round(work_pct), round(break_pct)
    # correct rounding error when e.g. work_pct = 55.5, break_pct = 45.5
    # after rounding work_pct = 56, break_pct = 46, combined = 101
    if work_pct + break_pct > 100:
        break_pct -= 1

    print(duration_to_str(work_duration, "Work duration"))
    print(duration_to_str(break_duration, "Break duration"))

    # Num work sessions, num break sessions
    num_work_sessions, num_break_sessions = get_num_work_break_sessions(log)
    print("Total work sessions:", num_work_sessions)
    print("Total break sessions:", num_break_sessions)
    print()

    # Work and break sessions in descending duration order
    work_sessions, break_sessions = get_work_break_sessions_desc(log)

    print("Work sessions")
    for sesh in work_sessions:
        start, end, duration = sesh
        print(
            f"{datetime_to_str(date, start)} - {datetime_to_str(date, end)}, "
            f"{duration_to_str(duration, 'duration')}"
        )

    print("\nBreak sessions")
    for sesh in break_sessions:
        start, end, duration = sesh
        print(
            f"{datetime_to_str(date, start)} - {datetime_to_str(date, end)}, "
            f"{duration_to_str(duration, 'duration')}"
        )


def print_stats_date_range(from_date: datetime.date, to_date: datetime.date) -> None:
    num_days = (to_date - from_date).days
    for i in range(num_days + 1):
        dt = from_date + datetime.timedelta(days=i)
        print_stats_single_date(dt)
        print()


def main(args):
    parser = ArgumentParser(prog=f"{config.program_name()} stats")
    parser.add_argument(
        "dates",
        nargs="+",
        help=(
            "'dd-mm-yy' format date. If one date provided then only show stats\n"
            "for that day. Otherwise if two dates provided then show stats for\n"
            "all dates in the inclusive range bounded by both dates."
        ),
        metavar="date",
        type=config.deserialise_date,
    )
    args = parser.parse_args(args)

    if len(args.dates) == 1:
        print_stats_single_date(args.dates[0])
    elif len(args.dates) == 2 and args.dates[0] <= args.dates[1]:
        print_stats_date_range(args.dates[0], args.dates[1])
    else:
        parser.print_help()
