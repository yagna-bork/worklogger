from argparse import ArgumentParser
import config


def init_config(logs_directory, editor_command):
    file_content = [
        f"logs_directory={logs_directory}\n",
        f"editor_command={editor_command}\n",
    ]
    with open(CONFIG_PATH, "w") as cfg:
        cfg.writelines(file_content)


def main(args):
    parser = ArgumentParser(usage="worklogger.py init [-h] log_director editor_command")
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


if "__name__" == "main":
    print("'initialise' is not a script. Use 'worklogger.py' instead")
