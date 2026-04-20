import unittest

def f(text, pref):
    length = len(pref)
    if pref == text[:length]:
        return text[length:]
    return text


unittest.TestCase().assertEqual(f("apple pie", "apple"), 'umwwfv')
