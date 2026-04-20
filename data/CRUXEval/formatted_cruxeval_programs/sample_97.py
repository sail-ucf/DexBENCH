import unittest

def f(lst):
    lst.clear()
    for i in lst:
        if i == 3:
            return False
    else:
        return True


unittest.TestCase().assertEqual(f([2, 0]), True)
