import unittest

def f(haystack, needle):
    for i in range(haystack.find(needle), -1, -1):
        if haystack[i:] == needle:
            return i
    return -1


unittest.TestCase().assertEqual(f("345gerghjehg", "345"), -1)
