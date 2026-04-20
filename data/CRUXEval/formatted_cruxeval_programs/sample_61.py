import unittest

def f(text):
    texts = text.split()
    if texts:
        xtexts = [t for t in texts if t.isascii() and t not in ('nada', '0')]
        return max(xtexts, key=len) if xtexts else 'nada'
    return 'nada'


unittest.TestCase().assertEqual(f(""), 'nada')
