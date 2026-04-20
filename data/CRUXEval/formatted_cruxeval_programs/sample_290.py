import unittest

def f(text, prefix):
    if text.startswith(prefix):
        return text.removeprefix(prefix)
    if prefix in text:
        return text.replace(prefix, '').strip()
    return text.upper()


unittest.TestCase().assertEqual(f('abixaaaily', 'al'), 'ABIXAAAILY')
