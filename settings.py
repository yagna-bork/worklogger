import config
from argparse import ArgumentParser


def main(args):
    parser = ArgumentParser(usage="worklogger.py settings [-h] [-s, --set]")
    parser.add_argument(
        "-s",
        "--set",
        nargs=2,
        metavar=("setting_name", "new_value"),
        help=f"Change setting_name's value to new_value.\nValid settings are {config.VALID_SETTINGS}",
    )
    args = parser.parse_args(args)

    if args.set is not None:
        setting_name, new_value = args.set
        if setting_name not in config.VALID_SETTINGS:
            parser.print_help()
        else:
            config.set_config(setting_name, new_value)
    else:
        config.print_config()


if "__name__" == "main":
    print("'settings' is not a script. Use 'worklogger.py' instead")
