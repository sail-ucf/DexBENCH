import unittest

def f(text, letter):
    if letter in text:
        start = text.index(letter)
        return text[start + 1:] + text[:start + 1]
    return text


unittest.TestCase().assertEqual(f('19kefp7', '9'), 'kefp719')
