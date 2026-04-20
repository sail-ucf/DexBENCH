import unittest

def f(text):
    for char in text:
        if not char.isspace():
            return False
    return True


unittest.TestCase().assertEqual(f('     i'), False)
