import unittest

def f(text, suffix):
    if suffix.startswith("/"):
        return text + suffix[1:]
    return text


unittest.TestCase().assertEqual(f('hello.txt', '/'), 'hello.txt')
