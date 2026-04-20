import unittest

def f(d, index):
    length = len(d.items())
    idx = index % length
    v = d.popitem()[1]
    for _ in range(idx):
        d.popitem()
    return v


unittest.TestCase().assertEqual(f({27:39}, 1), 39)
