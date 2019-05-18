#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import re
import subprocess
from typing import Iterable

from code_parser import start_parsing, PYTHON_FILES, JAVA_FILES
from data_out import print_results, TOP_VERBS_AMOUNT, VALID_OUTPUT_TYPES

allowed_file_extensions = {
    'python': PYTHON_FILES,
    'java': JAVA_FILES,
}
VALID_GITHUB_REPO_URL = r'^\/(gist\.)?github\.com\/[\w\-]+\/(?P<repo>[\w\-]+)'


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
    allowed_types = allowed_file_extensions.keys()
    if file_type not in allowed_types:
        raise argparse.ArgumentTypeError(f"Only {','.join(allowed_types)} file types parsing is implemented")
    return file_type


def check_github_url_validity(github_url: str) -> str:
    url_match = re.match(VALID_GITHUB_REPO_URL, github_url)
    if not url_match:
        raise argparse.ArgumentTypeError(f"{github_url}, is not a valid GitHub repo url")
    return github_url


def check_arg_range(value: str, valid_range: Iterable) -> str:
    if not value.lower() in valid_range:
        raise argparse.ArgumentTypeError(
            f"wrong value {value}, valid values are: {','.join(valid_range)}  default=console"
        )
    return value.lower()


def check_out_range(out_type: str):
    return check_arg_range(out_type, VALID_OUTPUT_TYPES)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='analyses use of verbs in functions names')
    source = ap.add_mutually_exclusive_group(required=True)  # source can be: local folder or github repo
    source.add_argument(
        "--repo",
        dest="repo",
        action="store",
        type=check_github_url_validity,
        help="github (or gist) repo URL to clone and analyse"
    )
    source.add_argument(
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
        dest="file_type",
        type=check_type_value,
        default='python',
        action="store",
        help=f"code file types: {','.join(PYTHON_FILES)} {','.join(JAVA_FILES)} default=.py"
    )
    ap.add_argument(
        '--out',
        dest='out_type',
        type=check_out_range,
        action='store',
        default='con',
        help=f'where to write analysis results, options are: {", ".join(VALID_OUTPUT_TYPES)} default=console'
    )
    args = ap.parse_args(sys.argv[1:])
    if args.repo:
        match = re.match(VALID_GITHUB_REPO_URL, args.repo)
        folder = match.group('repo')
        full_git_url = f'git:/{args.repo}.git'
        error = subprocess.call(['git', 'clone', full_git_url])
        if error:
            raise argparse.ArgumentTypeError(f'error {error} while cloning repo: {full_git_url}')
    else:
        folder = args.folder

    result_data = start_parsing(folder, file_extensions=allowed_file_extensions[args.file_type])

    print_results(results=result_data, start_folder=folder, output=args.out_type)
