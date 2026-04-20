import unittest

def f(array, index):
    if index < 0:
        index = len(array) + index
    return array[index]


unittest.TestCase().assertEqual(f([1], 0), 1)
