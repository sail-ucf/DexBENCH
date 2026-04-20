import unittest

def f(a, b):
    for key, value in b.items():
        if key not in a:
            a[key] = [value]
        else:
            a[key].append(value)
    return a


unittest.TestCase().assertEqual(f({}, {'foo': 'bar'}), {'foo': ['bar']})
