import unittest

def f(integer, n):
    i = 1
    text = str(integer)
    while (i+len(text) < n):
        i += len(text)
    return text.zfill(i+len(text))


unittest.TestCase().assertEqual(f(8999,2), '08999')
