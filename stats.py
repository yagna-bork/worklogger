import sys
from argparse import ArgumentParser


def main(args):
    parser = ArgumentParser()
    args = parser.parse_args(args)
    print("Not yet implemented", file=sys.stderr)


if "__name__" == "main":
    print("'stats' is not a script. Use 'worklogger.py' instead")
