import unittest

def f(t):
    for c in t:
        if not c.isnumeric():
            return False
    return True


unittest.TestCase().assertEqual(f('#284376598'), False)
