import string
import unittest

def f(string, encryption):
    if encryption == 0:
        return string
    else:
        return string.upper().encode('rot13')


unittest.TestCase().assertEqual(f('UppEr', 0), 'UppEr')
