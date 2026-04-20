import unittest

def f(text):
    a = text.strip().split(' ')
    for i in range(len(a)):
        if a[i].isdigit() is False:
            return '-'
    return " ".join(a)


unittest.TestCase().assertEqual(f("d khqw whi fwi bbn 41"), '-')
