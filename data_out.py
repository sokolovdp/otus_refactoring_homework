# -*- coding: utf-8 -*-
from collections import Counter
TOP_VERBS_AMOUNT = 10


def print_results(results: list):
    for result in results:
        top_verbs = Counter(result.verbs).most_common(TOP_VERBS_AMOUNT)
        print('\n file=', result.file, 'verbs=', result.verbs, 'top verbs=', top_verbs)
