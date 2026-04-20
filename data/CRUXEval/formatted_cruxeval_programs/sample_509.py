import unittest

def f(value, width):
    if value >= 0:
        return str(value).zfill(width)

    if value < 0:
        return '-' + str(-value).zfill(width)
    return ''


unittest.TestCase().assertEqual(f(5, 1), '5')
