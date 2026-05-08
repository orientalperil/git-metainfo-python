import argparse

from .core import write_git_metainfo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        default="git-metainfo.json",
        help="Output file path",
    )

    args = parser.parse_args()

    path = write_git_metainfo(args.output)

    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
