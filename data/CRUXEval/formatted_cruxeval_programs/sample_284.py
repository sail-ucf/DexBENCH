import unittest

def f(text, prefix):
    idx = 0
    for letter in prefix:
        if text[idx] != letter:
            return None
        idx += 1
    return text[idx:]


unittest.TestCase().assertEqual(f('bestest', 'bestest'), '')
