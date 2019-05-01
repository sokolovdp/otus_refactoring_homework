# -*- coding: utf-8 -*-
from collections import Counter

TOP_VERBS_AMOUNT = 10


def print_results(results: list, top_verbs_amount: int = TOP_VERBS_AMOUNT, start_folder=None):
    for result in results:
        file_name = result.file.replace(start_folder, '.') if start_folder else result.file
        if result.verbs:
            top_verbs = Counter(result.verbs).most_common(top_verbs_amount)
            print(f'file: {file_name} -> verbs {result.verbs}  top verbs{top_verbs}')
        else:
            print(f'file: {file_name} -> no verbs in function names!')
