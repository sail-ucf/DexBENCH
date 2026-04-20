import unittest

s = '<' * 10
def f(num):
    if num % 2 == 0:
        return s
    else:
        return num - 1


unittest.TestCase().assertEqual(f(21), 20)
