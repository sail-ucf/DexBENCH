import unittest

def f(total, arg):
    if type(arg) is list:
        for e in arg:
            total.extend(e)
    else:
        total.extend(arg)
    return total


unittest.TestCase().assertEqual(f([1, 2, 3], 'nammo'), [1, 2, 3, 'n', 'a', 'm', 'm', 'o'])
