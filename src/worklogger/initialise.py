from argparse import ArgumentParser
from pathlib import Path
from . import config


def main(args):
    parser = ArgumentParser(prog=f"{config.program_name()} init")
    parser.add_argument(
        "logs_directory",
        help=(
            "The directory where worklogs will be stored. "
            "It will be created if it doesn't exist"
        ),
        type=Path,
    )
    parser.add_argument(
        "editor_command",
        help="The command to invoke your editor of choice",
        type=lambda cmd: cmd.split(" "),
    )
    args = parser.parse_args(args)

    config.init_config(args.logs_directory, args.editor_command)
