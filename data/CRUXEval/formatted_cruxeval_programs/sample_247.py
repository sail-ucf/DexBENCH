import unittest

def f(s):
    if s.isalpha():
        return "yes"
    if s == "":
        return "str is empty"
    return "no"


unittest.TestCase().assertEqual(f('Boolean'), 'yes')
