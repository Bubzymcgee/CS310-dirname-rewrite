# Title:             dirname_rewrite.py
# Author:            Kyle Becker
# Date:              10/27/25
# Description:       This program is a python reimplementaiton of the GNU Coreutils dirname utility
# Implimented Flags: -a --multiple processes multiple paths, -p --parents Prints all parent directories
# Example Use Case:  python3 dirname_rewrite.py /usr/bin/sort

import os
import argparse
import sys


def dirname(path: str) -> str:
    """
    Returns the directory component of `path`,
    """
    if path == "":
        return "."

    # Remove trailing slashes (but keep root slash)
    while len(path) > 1 and path.endswith("/"):
        path = path[:-1]

    # Find last slash
    slash_index = path.rfind("/")

    if slash_index == -1:
        return "."
    elif slash_index == 0:
        return "/"
    else:
        return path[:slash_index]


def all_parents(path: str):
    """
    Yield all parent directories of a given path.
    For example: /usr/bin/sort -> /usr, /usr/bin
    """
    parents = []
    dir_part = dirname(path)
    while dir_part not in (".", "/") and dir_part not in parents:
        parents.append(dir_part)
        dir_part = dirname(dir_part)

    # Add root if applicable
    if dir_part == "/":
        parents.append("/")

    return parents[::-1]  # Return from top-down order


def main():
    parser = argparse.ArgumentParser(
        description="Strip last component from file name."
    )
    parser.add_argument(
        "-a", "--multiple",
        action="store_true",
        help="support multiple arguments"
    )
    parser.add_argument(
        "-p", "--parents",
        action="store_true",
        help="print all parent directories of the given path(s)"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="one or more pathnames"
    )

    args = parser.parse_args()

    # Handle multiple paths
    if args.multiple:
        for p in args.paths:
            if args.parents:
                for parent in all_parents(p):
                    sys.stdout.write(parent + "\n")
            else:
                sys.stdout.write(dirname(p) + "\n")
    else:
        path = args.paths[0]
        if args.parents:
            for parent in all_parents(path):
                sys.stdout.write(parent + "\n")
        else:
            sys.stdout.write(dirname(path) + "\n")


if __name__ == "__main__":
    main()