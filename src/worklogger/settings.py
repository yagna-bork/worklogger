import sys
from argparse import ArgumentParser

from . import config


def main(args):
    parser = ArgumentParser(prog=f"{config.program_name()} settings")
    parser.add_argument(
        "-s",
        "--set",
        nargs=2,
        metavar=("setting_name", "new_value"),
        help=f"Change setting_name's value to new_value.\nValid settings are {config.valid_settings()}",
        action="append",
        dest="settings",
    )
    args = parser.parse_args(args)

    # no optional args provided,
    # just display settings
    if args.settings is None:
        config.print_config()
        return

    # change setting for each valid optional arg
    for setting_name, new_value in args.settings:
        if setting_name not in config.valid_settings():
            print(
                f"Ignoring {setting_name}. Valid settings are {config.valid_settings()}",
                file=sys.stderr,
            )
            continue
        match setting_name:
            case "logs_directory":
                new_value = config.deserialise_logs_directory(new_value)
            case "editor_command":
                new_value = config.deserialise_editor_cmd(new_value)
        config.set_setting(setting_name, new_value)
