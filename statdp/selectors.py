from inspect import isfunction
import multiprocessing as mp
import numpy as np
import logging

logger = logging.getLogger(__name__)


class __EvaluateEvent:
    def __init__(self, a, b, epsilon, iterations):
        self.a = a
        self.b = b
        self.epsilon = epsilon
        self.iterations = iterations

    def __call__(self, s):
        cx = sum(1 for x in self.a if x in s)
        cy = sum(1 for y in self.b if y in s)
        cx, cy = (cx, cy) if cx > cy else (cy, cx)
        return cx, cy


_process_pool = mp.Pool(mp.cpu_count())


def event_selector(algorithm, args, kwargs, D1, D2, epsilon, iterations=100000, search_space=(), cores=0):
    assert isfunction(algorithm)
    from .core import test_statistics
    import math

    a = [algorithm(D1, *args, **kwargs) for _ in range(iterations)]
    b = [algorithm(D2, *args, **kwargs) for _ in range(iterations)]

    global _process_pool

    # find S which has minimum p value from search space
    threshold = 0.001 * iterations * np.exp(epsilon)

    results = list(map(__EvaluateEvent(a, b, epsilon, iterations), search_space)) if cores == 1 \
        else _process_pool.map(__EvaluateEvent(a, b, epsilon, iterations), search_space)

    p_values = [test_statistics(x[0], x[1], epsilon, iterations)
                if x[0] + x[1] > threshold else math.inf for x in results]

    for i, (s, (cx, cy), p) in enumerate(zip(search_space, results, p_values)):
        logger.debug('Event: %s p: %f cx: %d cy: %d ratio: %f' % (s, p, cx, cy, float(cy) / cx if cx != 0 else math.inf))

    return search_space[np.argmin(p_values)]