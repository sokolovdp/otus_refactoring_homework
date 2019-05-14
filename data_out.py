# -*- coding: utf-8 -*-
from collections import Counter
import json
from typing import List

from .code_parser import ParseResult

Results = List[ParseResult]
TOP_VERBS_AMOUNT = 10
VALID_OUTPUT_TYPES = ['json',  'con']
JSON_FILE = "code_analyse_result.json"


def write_json_file(results: ParseResult):
    with open(JSON_FILE, 'w', encoding='UTF-8') as json_file:
        json_file.write(json.dumps(results, sort_keys=True, indent=4, ensure_ascii=False))
    print('created file {} with analysis data'.format(JSON_FILE))


def print_results(
        output: str = 'con',
        results: Results = None,
        top_verbs_amount: int = TOP_VERBS_AMOUNT,
        start_folder=None
):
    if output == 'con':
        for result in results:
            file_name = result.file.replace(start_folder, '.') if start_folder else result.file
            if result.verbs:
                top_verbs = map(str, Counter(result.verbs).most_common(top_verbs_amount))
                print(f'file: {file_name} -> top verbs: {", ".join(top_verbs)}')
            else:
                print(f'file: {file_name} -> no verbs in function names!')
        print(f'--- processed {len(results)} files ---')
    elif output == 'json':
        write_json_file(results)
    else:
        raise NotImplementedError('Only "console" output is allowed!')
