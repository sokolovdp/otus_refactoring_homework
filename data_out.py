# -*- coding: utf-8 -*-
from collections import Counter
from typing import List

import code_parser

Results = List[code_parser.ParseResult]
TOP_VERBS_AMOUNT = 10
VALID_OUTPUT_TYPES = ['csv_file', 'console']
CSV_FILE = "code_analyse_result.csv"


def write_csv_file(results: list):
    with open(CSV_FILE, 'w', encoding='UTF-8') as csv_file:
        for result in results:
            top_verbs_string = [f'{str(tp).replace(",", "")}' for tp in result[1]]
            top_verbs_string = ','.join(top_verbs_string)
            csv_file.write(f'{result[0]},{top_verbs_string}')

    print(f'created file {CSV_FILE} with analysis data')


def write_to_console(results: list):
    for result in results:
        top_verbs_string = ', '.join(map(str, result[1]))
        print(f'file: {result[0]} -> top verbs: {top_verbs_string}')


writers_table = {
    'con': write_to_console,
    'csv': write_csv_file,
}


def print_results(output: str = 'con', results: Results = None, start_folder=None):
    formatted_results = []
    for result in results:
        file_name = result.file.replace(start_folder, '.') if start_folder else result.file
        top_verbs = Counter(result.verbs).most_common(TOP_VERBS_AMOUNT)
        formatted_results.append((file_name, list(top_verbs)))

    writer = writers_table[output]
    writer(formatted_results)
