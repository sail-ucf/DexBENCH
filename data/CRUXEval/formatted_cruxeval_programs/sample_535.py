import unittest

def f(n):
    for n in str(n):
        if n not in "012" and n not in list(range(5, 10)):
            return False
    return True


unittest.TestCase().assertEqual(f(1341240312), False)
