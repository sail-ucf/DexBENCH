import unittest

def f(array):
    d = dict(array)
    for key, value in d.items():
        if value < 0 or value > 9:
            return None
    return d


unittest.TestCase().assertEqual(f(((8, 5), (8, 2), (5, 3))), {8: 2, 5: 3})
