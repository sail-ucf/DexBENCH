import unittest

def f(text):
    if ',' in text:
        before, _, after = text.partition(',')
        return after + ' ' + before
    return ',' + text.partition(' ')[-1] + ' 0'


unittest.TestCase().assertEqual(f('244, 105, -90'), ' 105, -90 244')
