import unittest

def f(ets):
    while ets:
        k, v = ets.popitem()
        ets[k] = v**2
    return ets


unittest.TestCase().assertEqual(f({}), {})
