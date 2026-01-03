from argparse import ArgumentParser
import datetime

from . import config
from .log import LogEntry, parse_log, LogEntryType
from .util import timedelta_hours, timedelta_mins


def was_work_done(log):
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


def get_day_start_end_duration(log):
    start = log.entries[0].datetime
    end = log.entries[-1].datetime
    delta = end - start
    duration = {
        "hours": timedelta_hours(delta),
        "mins": timedelta_mins(delta),
        "total_mins": delta.seconds // 60,
    }
    return start, end, duration


def get_work_break_duration(log):
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

    work_duration = {
        "hours": timedelta_hours(time_worked),
        "mins": timedelta_mins(time_worked),
        "total_mins": time_worked.seconds // 60,
    }
    break_duration = {
        "hours": timedelta_hours(time_breaked),
        "mins": timedelta_mins(time_breaked),
        "total_mins": time_breaked.seconds // 60,
    }
    return work_duration, break_duration


def datetime_to_str(log_date, dt):
    """Str representation with date component if it's different to date of the log"""
    st = ""
    date, time = dt.date(), dt.time()
    if date != log_date:
        st += date.strftime(config.date_format())
    st += f" {time.strftime(config.time_format())}"
    return st


def print_stats_single_date(date):
    log = parse_log(date)

    date_str = config.serialise_date(date)
    print(date_str)
    print("-" * len(date_str))

    if not was_work_done(log):
        print(f"No work done on {date_str}")
        return

    # start of day, end of day, length of day
    start, end, duration = get_day_start_end_duration(log)
    print("Started:", datetime_to_str(date, start))
    print("Ended:", datetime_to_str(date, end))
    print("Duration:", duration["hours"], "hrs,", duration["mins"], "mins")

    # total time worked, total break time, above two as percentages of day
    work_duration, break_duration = get_work_break_duration(log)

    work_pct = work_duration["total_mins"] / duration["total_mins"] * 100
    break_pct = break_duration["total_mins"] / duration["total_mins"] * 100
    work_pct, break_pct = round(work_pct), round(break_pct)
    # correct rounding error when e.g. work_pct = 55.5, break_pct = 45.5
    # after rounding work_pct = 56, break_pct = 46, combined = 101
    if work_pct + break_pct > 100:
        break_pct -= 1

    print(
        "Work duration:",
        work_duration["hours"],
        "hrs,",
        work_duration["mins"],
        "mins",
        f"({work_pct}%)",
    )
    print(
        "Break duration:",
        break_duration["hours"],
        "hrs,",
        break_duration["mins"],
        "mins",
        f"({break_pct}%)",
    )

    print("Rest not yet implemented")
    # num work sessions, num break sessions
    # work sessions desc length order
    # break sessions desc length order


def print_stats_date_range(from_date, to_date):
    print("Range not yet implemented.")


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
    elif len(args.dates) == 2:
        print_stats_date_range(args.dates[0], args.dates[1])
    else:
        parser.print_help()
