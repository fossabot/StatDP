from statdp.algorithms import *


def test_noisymax():
    # add no noise to the array
    assert noisy_max_v1a([1, 2, 1], float('inf')) == 1
    assert noisy_max_v1b([1, 3, 1], float('inf')) == 3
    assert noisy_max_v2a([1, 3, 1], float('inf')) == 1
    assert noisy_max_v2b([1, 3, 1], float('inf')) == 3


def test_sparsevector():
    assert sparse_vector_1([1, 2, 3, 4], float('inf'), 1, 2) == 2
    assert sparse_vector_2([1, 2, 3, 4], float('inf'), 1, 1.5) == 1
    assert sparse_vector_3([1, 2, 3, 4], float('inf'), 1, 1.5) == 1
    assert sparse_vector_4([1, 2, 3, 4], float('inf'), 1, 1.5) == 1
    assert sparse_vector_2([1, 2, 3, 4], float('inf'), 1, 3.5) == 1
    assert sparse_vector_3([1, 2, 3, 4], float('inf'), 1, 3.5) == 1
    assert sparse_vector_4([1, 2, 3, 4], float('inf'), 1, 3.5) == 1
    assert sparse_vector_no_threshold_noise([1, 2, 3, 4], float('inf'), 1, 2.5) == 2
    assert sparse_vector_lyu([1, 2, 3, 4], float('inf'), 1, 2.5) == 2


def test_histogram():
    assert histogram([1, 2], float('inf')) == 1
    assert isinstance(histogram([1, 2], 1), float)
    assert histogram_eps([1, 2], 0) == 1
    assert isinstance(histogram_eps([1, 2], 1), float)


def test_laplace_mechanism():
    assert laplace_mechanism([1, 2, 3], float('inf')) == 1
