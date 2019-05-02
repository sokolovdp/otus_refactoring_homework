#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse

from code_parser import start_parsing, PYTHON_FILES
from data_out import print_results, TOP_VERBS_AMOUNT


def check_folder_is_readable(folder_name: str) -> str:
    if not os.path.isdir(folder_name):
        raise argparse.ArgumentTypeError(f"{folder_name} is not a valid path")
    if not os.access(folder_name, os.R_OK):
        raise argparse.ArgumentTypeError(f"{folder_name} is not a readable dir")
    return folder_name


def check_top_range(value: str) -> int:
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    if not 0 < int_value < TOP_VERBS_AMOUNT:
        raise argparse.ArgumentTypeError(f"{value} must be in range from 1 to {TOP_VERBS_AMOUNT}")
    return int_value


def check_type_value(file_type: str) -> str:
    if file_type != 'python':
        raise argparse.ArgumentTypeError(f"Only python files parsing is implemented")
    return file_type


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='analyses use of verbs in functions names')
    ap.add_argument(
        "--dir",
        dest="folder",
        action="store",
        type=check_folder_is_readable,
        default=os.getcwd(),
        help="folder with code to analyse, default folder is current"
    )
    ap.add_argument(
        "--top",
        dest="max_top",
        type=check_top_range,
        default=TOP_VERBS_AMOUNT,
        action="store",
        help=f"number of top used words, default={TOP_VERBS_AMOUNT}"
    )
    ap.add_argument(
        "--type",
        dest="file_types",
        type=check_type_value,
        default='python',
        action="store",
        help=f"code file types, default='python'"
    )
    args = ap.parse_args(sys.argv[1:])
    start_folder = args.folder
    top_verbs_amount = args.max_top

    result_data = start_parsing(start_folder, file_extensions=PYTHON_FILES)

    print_results(results=result_data, top_verbs_amount=top_verbs_amount, start_folder=start_folder)
