import unittest

def f(vectors):
    sorted_vecs = []
    for vec in vectors:
        vec.sort()
        sorted_vecs.append(vec)
    return sorted_vecs


unittest.TestCase().assertEqual(f([]), [])
