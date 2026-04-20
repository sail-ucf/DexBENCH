import unittest

def f(text, value):
    length = len(text)
    letters = list(text)
    if value not in letters:
        value = letters[0]
    return value * length


unittest.TestCase().assertEqual(f('ldebgp o', 'o'), 'oooooooo')
