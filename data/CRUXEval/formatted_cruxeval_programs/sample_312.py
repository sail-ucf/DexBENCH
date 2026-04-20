import unittest

def f(str):
    if str.isalnum():
        return "True"
    return "False"


unittest.TestCase().assertEqual(f('777'), 'True')
