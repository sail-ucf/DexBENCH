import unittest

def f(text, char):
    if char in text:
        text = [t.strip() for t in text.split(char) if t]
        if len(text) > 1:
            return True
    return False


unittest.TestCase().assertEqual(f('only one line', ' '), True)
