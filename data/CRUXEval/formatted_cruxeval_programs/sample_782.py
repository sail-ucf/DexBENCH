import unittest

def f(input):
    for char in input:
        if char.isupper():
            return False
    return True


unittest.TestCase().assertEqual(f("a j c n x X k"), False)
