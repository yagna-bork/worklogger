import sys
from argparse import ArgumentParser

import config


def main(args):
    parser = ArgumentParser(usage="worklogger.py settings [-h] [-s, --set]")
    parser.add_argument(
        "-s",
        "--set",
        nargs=2,
        metavar=("setting_name", "new_value"),
        help=f"Change setting_name's value to new_value.\nValid settings are {config.VALID_SETTINGS}",
        action="append",
        dest="settings",
    )
    args = parser.parse_args(args)

    if args.settings is None:
        config.print_config()
        return

    for setting_name, new_value in args.settings:
        if setting_name not in config.VALID_SETTINGS:
            print(
                f"Ignoring {setting_name}. Valid settings are {config.VALID_SETTINGS}",
                file=sys.stderr,
            )
            continue
        config.set_config(setting_name, new_value)


if "__name__" == "main":
    print("'settings' is not a script. Use 'worklogger.py' instead")
