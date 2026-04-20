import unittest

def f(text, space):
    if space < 0:
        return text
    return text.ljust(len(text) // 2 + space)


unittest.TestCase().assertEqual(f('sowpf', -7), 'sowpf')
