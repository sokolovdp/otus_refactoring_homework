#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import chardet
import asyncio
import aiofiles
from concurrent.futures import ALL_COMPLETED
from collections import namedtuple

from code_parser import PythonCodeParser, PYTHON_FILE_EXTENSIONS
from data_out import print_results

ParseResult = namedtuple('ParseResult', ['file', 'verbs'])


def build_list_of_files(path: str = None, extensions: list = None) -> list:
    files_in_the_path = []
    for path, sub_dirs, files in os.walk(path):
        for file_name in files:
            for extension in extensions:
                if file_name.endswith(extension):
                    full_path = os.path.join(path, file_name)
                    files_in_the_path.append(full_path)
    return files_in_the_path


async def read_from_file(file_name: str) -> str:
    try:
        async with aiofiles.open(file_name, 'rb') as file:
            raw_data = await file.read()
        encoding = chardet.detect(raw_data)['encoding']
        file_data = raw_data.decode(encoding)
    except IOError:
        file_data = ''
    return file_data


async def process_file(file_name: str, parser=None) -> ParseResult:
    file_content = await read_from_file(file_name)
    return ParseResult(file=file_name, verbs=parser.get_verbs_from_functions_names(file_content))


async def process_all_files(file_list: list, parser=None) -> list:
    futures = [process_file(file, parser) for file in file_list]
    done, pending = await asyncio.wait(futures, return_when=ALL_COMPLETED)
    analysis_data = [d.result() for d in done]
    return analysis_data


if __name__ == '__main__':
    code_file_extensions = PYTHON_FILE_EXTENSIONS
    code_parser = PythonCodeParser()
    start_folder = os.getcwd()
    folders_to_check = ['django', 'flask', ]
    files_to_analyse = []
    for folder in folders_to_check:
        current_path = os.path.join(start_folder, folder)
        files_to_analyse.extend(build_list_of_files(path=current_path, extensions=code_file_extensions))

    result_data = asyncio.run(
        process_all_files(files_to_analyse, parser=code_parser)
    )

    print_results(result_data)

