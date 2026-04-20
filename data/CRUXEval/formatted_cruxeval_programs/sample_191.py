import string
import unittest

def f(string):
    if string.isupper():
        return True
    else:
        return False


unittest.TestCase().assertEqual(f('Ohno'), False)
