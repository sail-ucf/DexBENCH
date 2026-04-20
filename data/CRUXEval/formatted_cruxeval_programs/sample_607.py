import unittest

def f(text):
    for i in ['.', '!', '?']:
        if text.endswith(i):
            return True
    return False


unittest.TestCase().assertEqual(f('. C.'), True)
