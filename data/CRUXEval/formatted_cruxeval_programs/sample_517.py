import unittest

def f(text):
    for i in range(len(text)-1, 0, -1):
        if not text[i].isupper():
            return text[0:i]
    return ''


unittest.TestCase().assertEqual(f('SzHjifnzog'), 'SzHjifnzo')
