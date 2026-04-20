import unittest

def f(text):
    if text.isascii():
        return 'ascii'
    else:
        return 'non ascii'


unittest.TestCase().assertEqual(f("u00e9"), 'ascii')
