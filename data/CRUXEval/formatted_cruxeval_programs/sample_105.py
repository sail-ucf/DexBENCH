import unittest

def f(text):
    if not text.istitle():
        return text.title()
    return text.lower()


unittest.TestCase().assertEqual(f("PermissioN is GRANTed"), 'Permission Is Granted')
