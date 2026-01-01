import sys
from argparse import ArgumentParser

from . import config


def main(args):
    parser = ArgumentParser(prog=f"{config.PROGRAM_NAME} settings")
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

    # no optional args provided
    if args.settings is None:
        config.print_config()
        return

    # change setting for each valid optional arg
    for setting_name, new_value in args.settings:
        if setting_name not in config.VALID_SETTINGS:
            print(
                f"Ignoring {setting_name}. Valid settings are {config.VALID_SETTINGS}",
                file=sys.stderr,
            )
            continue
        config.set_setting(setting_name, new_value)
