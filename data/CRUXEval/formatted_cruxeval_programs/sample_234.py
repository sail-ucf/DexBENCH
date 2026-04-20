import unittest

def f(text, char):
    position = len(text)
    if char in text:
        position = text.index(char)
        if position > 1:
            position = (position + 1) % len(text)
    return position


unittest.TestCase().assertEqual(f('wduhzxlfk', 'w'), 0)
