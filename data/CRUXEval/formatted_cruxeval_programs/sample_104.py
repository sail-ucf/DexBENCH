import unittest

def f(text):
    dic = dict()
    for char in text:
        dic[char] = dic.get(char, 0) + 1
    for key in dic:
        if dic[key] > 1:
            dic[key] = 1
    return dic


unittest.TestCase().assertEqual(f("a"), {'a': 1})
