# -*- coding: utf-8 -*-
from collections import Counter
TOP_VERBS_AMOUNT = 10


def print_results(results: list, top_verbs_amount: int = TOP_VERBS_AMOUNT):
    for result in results:
        if result.verbs:
            top_verbs = Counter(result.verbs).most_common(top_verbs_amount)
            print(f'file: {result.file} -> verbs {result.verbs}  top verbs{top_verbs}')
        else:
            print(f'file: {result.file} -> no verbs in function names!')
