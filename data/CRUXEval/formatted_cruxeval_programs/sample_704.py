import unittest

def f(s, n, c):
    width = len(c)*n
    for _ in range(width - len(s)):
        s = c + s
    return s


unittest.TestCase().assertEqual(f('.', 0, '99'), '.')
