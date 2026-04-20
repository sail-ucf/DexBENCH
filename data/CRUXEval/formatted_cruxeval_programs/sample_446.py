import unittest

def f(array):
    l = len(array)
    if l % 2 == 0:
        array.clear()
    else:
        array.reverse()
    return array


unittest.TestCase().assertEqual(f([]), [])
