import pytest
import numpy as np

from scipy.spatial.distance import cosine, euclidean
from projects.text_clustering.vector_sort import vector_sort

def test_256_dimensional_cosine_distance_as_default():
    input = np.random.rand(1000, 256)
    sorted_input = vector_sort(input)

    previous_distance = 0

    for index, vector in enumerate(sorted_input[1:]):
        distance = cosine(sorted_input[0], vector)
        assert distance > previous_distance, 'at index {}'.format(index)
        previous_distance = distance

def test_256_dimensional_euclidean_distance():
    input = np.random.rand(1000, 256)
    sorted_input = vector_sort(input, distance_fn=euclidean)

    previous_distance = 0

    for index, vector in enumerate(sorted_input[1:]):
        distance = euclidean(sorted_input[0], vector)
        assert distance > previous_distance, 'at index {}'.format(index)
        previous_distance = distance
