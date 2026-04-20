import unittest

def f(text):
    l = text.rpartition('0')
    if l[2] == '':
        return '-1:-1'
    return f'{len(l[0])}:{l[2].find("0") + 1}'


unittest.TestCase().assertEqual(f('qq0tt'), '2:0')
