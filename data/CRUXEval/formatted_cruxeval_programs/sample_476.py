import unittest

def f(a, split_on):
    t = a.split()
    a = []
    for i in t:
        for j in i:
            a.append(j)
    if split_on in a:
        return True
    else:
        return False


unittest.TestCase().assertEqual(f("booty boot-boot bootclass","o"), False)
