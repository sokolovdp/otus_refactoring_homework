#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import chardet
import asyncio
import aiofiles
import argparse
from concurrent.futures import ALL_COMPLETED
from collections import namedtuple

from code_parser import PythonCodeParser, PYTHON_FILE_EXTENSIONS
from data_out import print_results, TOP_VERBS_AMOUNT

ParseResult = namedtuple('ParseResult', ['file', 'verbs'])

START_FOLDER = os.getcwd()
MAX_NUMBER_OF_FILES = 100

INTERNAL_PYTHON_FOLDERS = {
    'venv',
    'bin',
    'lib',
    '.idea',
    '__pycache__',
    '.git'
}


def build_list_of_files(path: str = None, extensions: list = None) -> list:
    files_in_the_path = []
    for root, sub_dirs, files in os.walk(path):
        sub_dirs[:] = [d for d in sub_dirs if d not in INTERNAL_PYTHON_FOLDERS]
        for file_name in files:
            for extension in extensions:
                if file_name.endswith(extension):
                    full_path = os.path.join(root, file_name)
                    files_in_the_path.append(full_path)
    return files_in_the_path


async def read_from_file(file_name: str) -> str:
    try:
        async with aiofiles.open(file_name, 'rb') as file:
            raw_data = await file.read()
        if raw_data:
            encoding = chardet.detect(raw_data)['encoding']
            file_data = raw_data.decode(encoding)
        else:
            file_data = None
    except (IOError, Exception):
        file_data = None
    return file_data


async def process_file(file_name: str, parser=None) -> ParseResult:
    file_content = await read_from_file(file_name)
    if file_content is not None:
        result = ParseResult(file=file_name, verbs=parser.get_verbs_from_functions_names(file_content))
    else:
        result = ParseResult(file=file_name, verbs=[])
    return result


async def process_all_files(file_list: list, parser=None) -> list:
    futures = [process_file(file, parser) for file in file_list]
    done, pending = await asyncio.wait(futures, return_when=ALL_COMPLETED)
    analysis_data = [d.result() for d in done if d.result is not None]
    return analysis_data


def check_folder_is_readable(folder_name: str) -> str:
    if not os.path.isdir(folder_name):
        raise argparse.ArgumentTypeError(f"{folder_name} is not a valid path")
    if not os.access(folder_name, os.R_OK):
        raise argparse.ArgumentTypeError(f"{folder_name} is not a readable dir")
    return folder_name


def check_int_range(value: str) -> int:
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    if not 0 < int_value < TOP_VERBS_AMOUNT:
        raise argparse.ArgumentTypeError(f"{value} must be in range from 1 to {TOP_VERBS_AMOUNT}")
    return int_value


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='analyses use of verbs in functions names')
    ap.add_argument(
        "--dir",
        dest="folder",
        action="store",
        type=check_folder_is_readable,
        default=START_FOLDER,
        help="folder with code to analyse, default folder is current"
    )
    ap.add_argument(
        "--top",
        dest="max_top",
        type=check_int_range,
        default=TOP_VERBS_AMOUNT,
        action="store",
        help=f"number of top used words, default={TOP_VERBS_AMOUNT}"
    )
    args = ap.parse_args(sys.argv[1:])
    start_folder = args.folder
    top_verbs_amount = args.max_top
    code_file_extensions = PYTHON_FILE_EXTENSIONS
    code_parser = PythonCodeParser()

    files_to_analyse = build_list_of_files(path=start_folder, extensions=code_file_extensions)[:MAX_NUMBER_OF_FILES]

    result_data = asyncio.run(
        process_all_files(files_to_analyse, parser=code_parser)
    )

    print_results(result_data, top_verbs_amount=top_verbs_amount, start_folder=start_folder)
