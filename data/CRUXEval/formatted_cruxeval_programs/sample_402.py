import unittest

def f(n, l):
    archive = {}
    for _ in range(n):
        archive.clear()
        archive.update({x + 10: x * 10 for x in l})
    return archive


unittest.TestCase().assertEqual(f(0, ['aaa', 'bbb']), {})
