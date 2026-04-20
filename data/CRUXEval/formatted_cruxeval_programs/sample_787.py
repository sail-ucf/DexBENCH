import unittest

def f(text):
    if len(text) == 0:
        return ''
    text = text.lower()
    return text[0].upper() + text[1:]


unittest.TestCase().assertEqual(f('xzd'), 'Xzd')
