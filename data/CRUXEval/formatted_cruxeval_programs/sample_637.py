import unittest

def f(text):
    text = text.split(' ')
    for t in text:
        if not t.isnumeric():
            return 'no'
    return 'yes'


unittest.TestCase().assertEqual(f('03625163633 d'), 'no')
