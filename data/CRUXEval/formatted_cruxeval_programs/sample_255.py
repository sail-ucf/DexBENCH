import unittest

def f(text, fill, size):
    if size < 0:
        size = -size
    if len(text) > size:
        return text[len(text) - size:]
    return text.rjust(size, fill)


unittest.TestCase().assertEqual(f('no asw', 'j', 1), 'w')
