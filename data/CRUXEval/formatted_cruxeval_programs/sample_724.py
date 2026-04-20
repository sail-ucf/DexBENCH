import unittest

def f(text, function):
    cites = [len(text[text.index(function) + len(function):])]
    for char in text:
        if char == function:
            cites.append(len(text[text.index(function) + len(function):]))
    return cites


unittest.TestCase().assertEqual(f("010100", "010"), [3])
