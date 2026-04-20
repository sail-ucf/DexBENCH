import unittest

def f(text):
    freq = dict()
    for c in text.lower():
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return freq


unittest.TestCase().assertEqual(f("HI"), {'h': 1, 'i': 1})
