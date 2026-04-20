import unittest

def f(dct):
    values = dct.values()
    result = {}
    for value in values:
        item = value.split('.')[0]+'@pinc.uk'
        result[value] = item
    return result


unittest.TestCase().assertEqual(f({}), {})
