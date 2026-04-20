import unittest

def f(string):
    while string:
        if string[-1].isalpha():
            return string
        string = string[:-1]
    return string


unittest.TestCase().assertEqual(f('--4/0-209'), '')
