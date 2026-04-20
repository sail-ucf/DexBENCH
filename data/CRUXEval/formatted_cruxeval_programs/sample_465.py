import unittest

def f(seq, value):
    roles = dict.fromkeys(seq, 'north')
    if value:
        roles.update(key.strip() for key in value.split(', '))
    return roles


unittest.TestCase().assertEqual(f(['wise king', 'young king'], ''), {'wise king': 'north', 'young king': 'north'})
