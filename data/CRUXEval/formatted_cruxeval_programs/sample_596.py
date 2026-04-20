import unittest

def f(txt, alpha):
    txt = sorted(txt)
    if txt.index(alpha) % 2 == 0:
        return txt[::-1]
    return txt


unittest.TestCase().assertEqual(f(['8', '9', '7', '4', '3', '2'], '9'), ['2', '3', '4', '7', '8', '9'])
