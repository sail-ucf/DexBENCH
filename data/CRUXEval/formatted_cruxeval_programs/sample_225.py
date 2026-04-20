import unittest

def f(text):
    if text.islower():
        return True
    return False


unittest.TestCase().assertEqual(f("54882"), False)
