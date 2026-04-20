import unittest

def f(l1, l2):
    if len(l1) != len(l2):
        return {}
    return dict.fromkeys(l1, l2)


unittest.TestCase().assertEqual(f(['a', 'b'], ['car', 'dog']), {'a': ['car', 'dog'], 'b': ['car', 'dog']})
