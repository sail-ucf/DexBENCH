import string
import unittest

def f(string):
    if string.isupper():
        return string.lower()
    elif string.islower():
        return string.upper()
    return string


unittest.TestCase().assertEqual(f("cA"), 'cA')
