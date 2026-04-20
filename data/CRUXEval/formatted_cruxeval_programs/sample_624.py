import unittest

def f(text, char):
    char_index = text.find(char)
    result = []
    if char_index > 0:
        result = list(text[:char_index])
    result.extend(list(char)+list(text[char_index+len(char):]))
    return ''.join(result)


unittest.TestCase().assertEqual(f("llomnrpc","o"), 'xllomnrpc')
