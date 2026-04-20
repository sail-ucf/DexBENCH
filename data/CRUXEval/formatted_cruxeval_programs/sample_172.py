import unittest

def f(array):
    for i in range(len(array)):
        if array[i] < 0:
            array.pop(i)
    return array


unittest.TestCase().assertEqual(f([]), [])
