import unittest

def f(array, L):
    if L <= 0:
        return array
    if len(array) < L:
        array.extend(f(array, L - len(array)))
    return array


unittest.TestCase().assertEqual(f([1, 2, 3], 4), [1, 2, 3, 1, 2, 3])
