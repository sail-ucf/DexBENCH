import unittest

def f(text, value):
    if isinstance(value, str):
        return text.count(value) + text.count(value.lower())
    return text.count(value)


unittest.TestCase().assertEqual(f('eftw{ьТсk_1', '\\'), 0)
