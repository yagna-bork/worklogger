from argparse import ArgumentParser
from . import config


def main(args):
    parser = ArgumentParser(prog=f"{config.PROGRAM_NAME} init")
    parser.add_argument(
        "logs_directory",
        help="The directory where worklogs will be stored. Will be created if doesn't exist",
    )
    parser.add_argument(
        "editor_command",
        help="The command to invoke your editor of choice",
    )
    args = parser.parse_args(args)

    config.init_config(args.logs_directory, args.editor_command)
