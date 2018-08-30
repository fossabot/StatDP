from inspect import isfunction
import multiprocessing as mp
import numpy as np
from collections import Counter
from intervals import Interval
import logging

logger = logging.getLogger(__name__)


class __EvaluateEvent:
    def __init__(self, a, b, iterations):
        self.a = a
        self.b = b
        self.iterations = iterations

    def __call__(self, s):
        cx = sum(1 for x in self.a if x in s)
        cy = sum(1 for y in self.b if y in s)
        cx, cy = (cx, cy) if cx > cy else (cy, cx)
        return cx, cy


_process_pool = mp.Pool(mp.cpu_count())


def select_event(algorithm, input_list, epsilon, iterations=100000, search_space=None, cores=0):
    assert isfunction(algorithm)
    from .core import test_statistics

    input_event_pairs = []
    p_values = []

    for (d1, d2, kwargs) in input_list:
        result_d1 = [algorithm(d1, **kwargs) for _ in range(iterations)]
        result_d2 = [algorithm(d2, **kwargs) for _ in range(iterations)]

        if search_space is None:
            # determine the search space based on the return type
            # a subset of results to determine return type
            sub_result = result_d1 + result_d2
            counter = Counter(sub_result)

            # categorical output
            if len(counter) < iterations * 0.02 * 0.1:
                search_space = tuple((key,) for key in counter.keys())
            else:
                sub_result_sorted = np.sort(sub_result)
                average = np.average(sub_result_sorted)
                idx = np.searchsorted(sub_result_sorted, average, side='left')
                # find the densest 70% range
                search_min = int(idx - 0.35 * len(sub_result_sorted)) if int(idx - 0.4 * len(sub_result_sorted)) > 0 else 0
                search_max = int(0.7 * len(sub_result_sorted) - (idx - search_min))

                search_space = tuple(Interval((-float('inf'), alpha)) for alpha in
                                     np.linspace(sub_result_sorted[search_min], sub_result_sorted[search_max], num=25))

            logger.info('search space is set to {0}'.format(search_space))

        global _process_pool

        threshold = 0.001 * iterations * np.exp(epsilon)

        results = list(map(__EvaluateEvent(result_d1, result_d2, iterations), search_space)) if cores == 1 \
            else _process_pool.map(__EvaluateEvent(result_d1, result_d2, iterations), search_space)

        input_p_values = [test_statistics(cx, cy, epsilon, iterations)
                          if cx + cy > threshold else float('inf') for (cx, cy) in results]

        for (s, (cx, cy), p) in zip(search_space, results, input_p_values):
            logger.debug('d1: %s | d2: %s | event: %s | p: %f | cx: %d | cy: %d | ratio: %f' %
                         (d1, d2, s, p, cx, cy, float(cy) / cx if cx != 0 else float('inf')))

        input_event_pairs.extend(list((d1, d2, kwargs, event) for event in search_space))
        p_values.extend(input_p_values)

    # find an (d1, d2, kwargs, event) pair which has minimum p value from search space
    return input_event_pairs[np.argmin(p_values)]
