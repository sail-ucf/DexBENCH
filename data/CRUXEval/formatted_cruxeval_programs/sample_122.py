import string
import unittest

def f(string):
    if string[:4] != 'Nuva':
        return 'no'
    else:
        return string.rstrip()


unittest.TestCase().assertEqual(f('Nuva?dlfuyjys'), 'Nuva?dlfuyjys')
