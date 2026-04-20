import unittest

def f(s, x):
    count = 0
    while s[:len(x)] == x and count < len(s)-len(x):
        s = s[len(x):]
        count += len(x)
    return s


unittest.TestCase().assertEqual(f('If you want to live a happy life! Daniel', 'Daniel'), 'If you want to live a happy life! Daniel')
