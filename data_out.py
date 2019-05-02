# -*- coding: utf-8 -*-
from collections import Counter

TOP_VERBS_AMOUNT = 10


def print_results(
        output: str = 'console',
        results: list = None,
        top_verbs_amount: int = TOP_VERBS_AMOUNT,
        start_folder=None
):
    if output == 'console':
        for result in results:
            file_name = result.file.replace(start_folder, '.') if start_folder else result.file
            if result.verbs:
                top_verbs = map(str, Counter(result.verbs).most_common(top_verbs_amount))
                print(f'file: {file_name} -> top verbs: {", ".join(top_verbs)}')
            else:
                print(f'file: {file_name} -> no verbs in function names!')
        print(f'--- processed {len(results)} files ---')
    else:
        raise NotImplementedError('Only "console" output is allowed!')
