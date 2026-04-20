import unittest

def f(c, index, value):
    c[index] = value
    if value >= 3:
        c.update({'message' : 'xcrWt'})
    else:
        del c['message']
    return c


unittest.TestCase().assertEqual(f({1: 2, 3: 4, 5: 6, 'message': 'qrTHo'}, 8, 2), {1: 2, 3: 4, 5: 6, 8: 2})
