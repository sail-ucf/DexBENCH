import unittest

def f(sentence):
    for c in sentence:
        if c.isascii() is False:
            return False
        else:
            continue
    return True


unittest.TestCase().assertEqual(f('1z1z1'), True)
