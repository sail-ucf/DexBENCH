import unittest

def f(length, text):
    if len(text) == length:
        return text[::-1]
    return False


unittest.TestCase().assertEqual(f(-5, 'G5ogb6f,c7e.EMm'), False)
