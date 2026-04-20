import unittest

def f(text):
    text = text.upper()
    count_upper = 0
    for char in text:
        if char.isupper():
            count_upper += 1
        else:
            return 'no'
    return count_upper // 2


unittest.TestCase().assertEqual(f('ax'), 1)
