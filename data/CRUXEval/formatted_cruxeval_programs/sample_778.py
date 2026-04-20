import unittest

def f(prefix, text):
    if text.startswith(prefix):
        return text
    else:
        return prefix + text


unittest.TestCase().assertEqual(f('mjs', 'mjqwmjsqjwisojqwiso'), 'mjsmjqwmjsqjwisojqwiso')
