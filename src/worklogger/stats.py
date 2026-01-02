import datetime
from argparse import ArgumentParser

from . import config
from .log import parse_log, LogEntryType


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


def get_day_start_end_length(log):
    start = log.entries[0].datetime
    end = log.entries[-1].datetime
    # in minutes
    length = (end - start).seconds // 60
    return start, end, length


def print_stats_single_date(date):
    log = parse_log(date)

    date_str = config.serialise_date(date)
    print(date_str)
    print("-" * len(date_str))

    if not was_work_done(log):
        print(f"No work done on {date.strftime(config.date_format())}")
        return

    print("Rest not yet implemented")

    # start of day, end of day, length of day
    start, end, length = get_day_start_end_length(log)

    # total time worked, total break time, above two as percentages of day
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
