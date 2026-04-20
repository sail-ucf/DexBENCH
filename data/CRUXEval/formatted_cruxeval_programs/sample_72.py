import unittest

def f(text):
    for c in text:
        if not c.isnumeric():
            return False
    return bool(text)


unittest.TestCase().assertEqual(f('99'), True)
