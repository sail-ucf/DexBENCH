import unittest

def f(text, position, value):
    length = len(text)
    index = (position % (length + 2)) - 1
    if index >= length or index < 0:
        return text
    text[index] = value
    return ''.join(text)


unittest.TestCase().assertEqual(f("1zd", 0, 'm'), '1zd')
