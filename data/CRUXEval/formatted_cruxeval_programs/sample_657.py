import unittest

def f(text):
    for punct in '!.?,:;':
        if text.count(punct) > 1:
            return 'no'
        if text.endswith(punct):
            return 'no'
    return text.title()


unittest.TestCase().assertEqual(f("djhasghasgdha"), 'Djhasghasgdha')
