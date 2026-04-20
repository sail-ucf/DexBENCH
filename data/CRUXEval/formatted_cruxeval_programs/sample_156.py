import unittest

def f(text, limit, char):
    if limit < len(text):
        return text[0:limit]
    return text.ljust(limit, char)


unittest.TestCase().assertEqual(f('tqzym', 5, 'c'), 'tqzym')
