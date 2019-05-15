# -*- coding: utf-8 -*-
from collections import Counter
import json
from typing import List

import code_parser


Results = List[code_parser.ParseResult]
TOP_VERBS_AMOUNT = 10
VALID_OUTPUT_TYPES = ['json',  'con']
CSV_FILE = "code_analyse_result.json"


def write_csv_file(results: Results, start_folder: str):
    with open(CSV_FILE, 'w', encoding='UTF-8') as json_file:
        json_file.write(json.dumps(results, sort_keys=True, indent=4, ensure_ascii=False))
    print('created file {} with analysis data'.format(CSV_FILE))


def write_to_console(results: Results, start_folder: str):
    # for result in results:
    #     file_name = result.file.replace(start_folder, '.') if start_folder else result.file
    #     if result.verbs:
    #         top_verbs = map(str, Counter(result.verbs).most_common(top_verbs_amount))
    #         print(f'file: {file_name} -> top verbs: {", ".join(top_verbs)}')
    #     else:
    #         print(f'file: {file_name} -> no verbs in function names!')
    print(f'--- processed {len(results)} files ---')


def print_results(
        output: str = 'con',
        results: Results = None,
        top_verbs_amount: int = TOP_VERBS_AMOUNT,
        start_folder=None
):
    # if result.verbs:
    #     top_verbs = map(str, Counter(result.verbs).most_common(top_verbs_amount))
    #     print(f'file: {file_name} -> top verbs: {", ".join(top_verbs)}')
    # else:
    #     print(f'file: {file_name} -> no verbs in function names!')
    #
    # if output == 'con':
    #
    # elif output == 'csv':
    #     write_csv_file(results)
    # else:
    #     raise NotImplementedError('Only "console" output is allowed!')

    pass