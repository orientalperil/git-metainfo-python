import argparse
import json
import sys

from .core import get_git_data
from .core import write_git_metainfo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    data = get_git_data()

    if args.output:
        write_git_metainfo(args.output, data)
    else:
        json.dump(data, sys.stdout, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
