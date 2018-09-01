from statdp.algorithms import noisy_max_v1a, noisy_max_v1b
from statdp.selectors import select_event


def test_select_event():
    d1 = [0] + [2 for _ in range(4)]
    d2 = [1 for _ in range(5)]
    _, _, _, event = select_event(noisy_max_v1a, [(d1, d2, {'eps': 0.5})], 0.5, 100000, cores=0)
    assert 0 in event
    _, _, _, event = select_event(noisy_max_v1b, [(d1, d2, {'eps': 0.5})], 0.5, 100000, cores=0)
    assert 0 in event

