import unittest

def f(text):
    if text.upper() == text:
        return 'ALL UPPERCASE'
    return text


unittest.TestCase().assertEqual(f('Hello Is It MyClass'), 'Hello Is It MyClass')
