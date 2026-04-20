import string
import unittest

def f(string, prefix):
    if string.startswith(prefix):
        return string.removeprefix(prefix)
    return string


unittest.TestCase().assertEqual(f("Vipra", "via"), 'Vipra')
