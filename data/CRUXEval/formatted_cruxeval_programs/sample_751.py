import unittest

def f(text, char, min_count):
    count = text.count(char)
    if count < min_count:
        return text.swapcase()
    return text


unittest.TestCase().assertEqual(f("wwwwhhhtttpp", 'w', 3), 'wwwwhhhtttpp')
