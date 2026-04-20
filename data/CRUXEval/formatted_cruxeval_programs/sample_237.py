import unittest

def f(text, char):
    if char in text:
        suff, char, pref = text.partition(char)
        pref = suff[:-len(char)] + suff[len(char):] + char + pref
        return suff + char + pref
    return text


unittest.TestCase().assertEqual(f('uzlwaqiaj', 'u'), 'uuzlwaqiaj')
