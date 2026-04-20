import unittest

def f(text):
    if not text.strip():
        return len(text.strip())
    return None


unittest.TestCase().assertEqual(f(" \t "), 0)
