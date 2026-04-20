import unittest

def f(alphabet, s):
    a = [x for x in alphabet if x.upper() in s]
    if s.upper() == s:
        a.append('all_uppercased')
    return a


unittest.TestCase().assertEqual(f("abcdefghijklmnopqrstuvwxyz","UPPERCASED # % ^ @ ! VZ."), [])
