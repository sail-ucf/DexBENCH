import unittest

def f(n, m, text):
    if text.strip() == '':
        return text
    head, mid, tail = text[0], text[1:-1], text[-1]
    joined = head.replace(n, m) + mid.replace(n, m) + tail.replace(n, m)
    return joined


unittest.TestCase().assertEqual(f("x", "$", "2xz&5H3*1a@#a*1hris"), '2$z&5H3*1a@#a*1hris')
