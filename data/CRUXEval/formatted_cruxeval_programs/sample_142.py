import unittest

def f(x):
    if x.islower():
        return x
    else:
        return x[::-1]


unittest.TestCase().assertEqual(f('ykdfhp'), 'ykdfhp')
