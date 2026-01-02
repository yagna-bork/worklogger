import sys
from argparse import ArgumentParser

from .initialise import main as initialise_main
from .settings import main as settings_main
from .edit import main as edit_main
from .stats import main as stats_main
from . import config


def main():
    parser = ArgumentParser(prog=config.program_name())

    # Initally only init mode is allowed
    if not config.is_config_initialised():
        parser = ArgumentParser(prog="worklogger")
        parser.add_argument(
            "mode",
            choices=["init"],
            help=(
                "Select mode.\n"
                "init: Initialise configuration. Must be run as the first command\n"
            ),
        )
        parser.parse_args(sys.argv[1:2])
        initialise_main(sys.argv[2:])
        return

    # Once the config is created, the other options are allowed
    parser.add_argument(
        "mode",
        choices=["init", "settings", "edit", "stats"],
        help=(
            "Select mode.\n"
            "init: Initialise configuration. Must be run as the first command\n"
            "settings: Edit or see the configuration\n"
            "edit: Edit today's worklog\n"
            "stats: See some stats about your worklogs\n"
        ),
    )
    args = parser.parse_args(sys.argv[1:2])

    unparsed_args = sys.argv[2:]
    match args.mode:
        case "init":
            initialise_main(unparsed_args)
        case "settings":
            settings_main(unparsed_args)
        case "edit":
            edit_main(unparsed_args)
        case "stats":
            stats_main(unparsed_args)
