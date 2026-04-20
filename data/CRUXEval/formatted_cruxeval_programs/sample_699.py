import unittest

def f(text, elem):
    if elem != '':
        while text.startswith(elem):
            text = text.replace(elem, '')
        while elem.startswith(text):
            elem = elem.replace(text, '')
    return [elem, text]


unittest.TestCase().assertEqual(f("some", "1"), ['1', 'some'])
