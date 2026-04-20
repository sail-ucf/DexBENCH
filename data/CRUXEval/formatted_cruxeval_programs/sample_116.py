import unittest

def f(d, count):
    for i in range(count):
        if d == {}:
            break
        d.popitem()
    return d


unittest.TestCase().assertEqual(f({}, 200), {})
