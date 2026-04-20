import string
import unittest

def f(string):
    if string.isalnum():
        return "ascii encoded is allowed for this language"
    return "more than ASCII"


unittest.TestCase().assertEqual(f('Str zahrnuje anglo-ameriæske vasi piscina and kuca!'), 'more than ASCII')
