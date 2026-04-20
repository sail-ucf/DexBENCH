import unittest

def f(text):
    for i in range(len(text)):
        if text[0:i].startswith("two"):
            return text[i:]
    return 'no'


unittest.TestCase().assertEqual(f("2two programmers"), 'no')
