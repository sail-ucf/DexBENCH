import unittest

def f(a, b):
    if b in a:
        return b.join(a.partition(a[a.index(b) + 1]))
    else:
        return a


unittest.TestCase().assertEqual(f('sierizam', 'iz'), 'sieriizzizam')
