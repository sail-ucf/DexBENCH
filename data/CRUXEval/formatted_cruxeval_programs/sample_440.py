import unittest

def f(text):
    if text.isdecimal():
        return 'yes'
    else:
        return 'no'


unittest.TestCase().assertEqual(f("abc"), 'no')
