import unittest

def f(text, suffix):
    if suffix == '':
        suffix = None
    return text.endswith(suffix)


unittest.TestCase().assertEqual(f('uMeGndkGh', 'kG'), False)
