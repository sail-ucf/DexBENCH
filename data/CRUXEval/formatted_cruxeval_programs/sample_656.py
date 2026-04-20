import unittest

def f(letters):
    a = []
    for i in range(len(letters)):
        if letters[i] in a:
            return 'no'
        a.append(letters[i])
    return 'yes'


unittest.TestCase().assertEqual(f(['b', 'i', 'r', 'o', 's', 'j', 'v', 'p']), 'yes')
