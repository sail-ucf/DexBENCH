import unittest

def f(items, target):
    if target in items:
        return items.index(target)
    return -1


unittest.TestCase().assertEqual(f(['''1''', '+', '-', '**', '//', '*', '+'], '**'), 3)
