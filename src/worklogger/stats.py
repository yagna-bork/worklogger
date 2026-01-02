import datetime
from argparse import ArgumentParser

from . import config
from .log import parse_log_file


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
    start = log.entries[0].datetime
    end = log.entries[-1].datetime
    length = end - start
    return start, end, length


def print_stats_single_date(date):
    log = get_log(date)

    if not was_any_work_done(log):
        print(f"No work done on {date.strftime(config.date_format())}")
        return

    # start of day, end of day, length of day
    start, end, length = get_day_start_end_length(log)

    # total time worked, total break time, above two as percentages of day
    # work sessions desc length order
    # break sessions desc length order


def print_stats_date_range(from_date, to_date):
    print("Range not yet implemented.")


def main(args):
    parser = ArgumentParser(prog=f"{config.PROGRAM_NAME} stats")
    # TODO type conversion
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
