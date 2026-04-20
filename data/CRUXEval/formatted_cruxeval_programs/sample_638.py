import unittest

def f(s, suffix):
    if not suffix:
        return s
    while s.endswith(suffix):
        s = s[:-len(suffix)]
    return s


unittest.TestCase().assertEqual(f('ababa', 'ab'), 'ababa')
