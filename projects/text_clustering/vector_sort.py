import numpy as np
from scipy.spatial.distance import cosine

'''
sorts list in increasing distance based on some distance function
and mergesort

Time Complexity: O(nlog(n))
Memory Complexity O(n)
'''
def vector_sort(vectors, distance_fn=cosine):
    ref_vector = vectors[0]

    def compare_fn(a, b):
        dist_a = distance_fn(ref_vector, a)
        dist_b = distance_fn(ref_vector, b)
        if dist_a < dist_b:
            return -1
        elif dist_a > dist_b:
            return 1
        else:
            return 0

    return sorted(vectors, cmp=compare_fn)
