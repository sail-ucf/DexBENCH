import unittest

def f(doc):
    for x in doc:
        if x.isalpha():
            return x.capitalize()
    return '-'


unittest.TestCase().assertEqual(f('raruwa'), 'R')
