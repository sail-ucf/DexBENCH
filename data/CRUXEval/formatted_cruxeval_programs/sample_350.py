import unittest

def f(d):
    size = len(d)
    v = [0] * size
    if size == 0:
        return v
    for i, e in enumerate(d.values()):
        v[i] = e
    return v


unittest.TestCase().assertEqual(f({'a': 1, 'b': 2, 'c': 3}), [1, 2, 3])
