import unittest

def f(name):
    if name.islower():
        name = name.upper()
    else:
        name = name.lower()
    return name


unittest.TestCase().assertEqual(f('Pinneaple'), 'pinneaple')
