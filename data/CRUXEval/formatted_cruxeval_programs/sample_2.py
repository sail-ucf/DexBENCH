import unittest

def f(text):
    new_text = list(text)
    for i in '+':
        if i in new_text:
            new_text.remove(i)
    return ''.join(new_text)


unittest.TestCase().assertEqual(f('hbtofdeiequ'), 'hbtofdeiequ')
