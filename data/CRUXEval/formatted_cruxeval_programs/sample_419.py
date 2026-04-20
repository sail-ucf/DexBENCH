import unittest

def f(text, value):
    if not value in text:
        return ''
    return text.rpartition(value)[0]


unittest.TestCase().assertEqual(f('mmfbifen', 'i'), 'mmfb')
