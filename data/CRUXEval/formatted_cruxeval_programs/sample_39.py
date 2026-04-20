import unittest

def f(array, elem):
    if elem in array:
        return array.index(elem)
    return -1


unittest.TestCase().assertEqual(f([6, 2, 7, 1], 6), 0)
