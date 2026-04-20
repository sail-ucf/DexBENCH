import unittest

def f(text, s, e):
    sublist = text[s:e]
    if not sublist:
        return -1
    return sublist.index(min(sublist))


unittest.TestCase().assertEqual(f('happy', 0, 3), 1)
