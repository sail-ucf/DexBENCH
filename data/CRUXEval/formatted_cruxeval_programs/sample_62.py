import unittest

def f(user):
    if len(list(user.keys())) > len(list(user.values())):
        return tuple(user.keys())
    return tuple(user.values())


unittest.TestCase().assertEqual(f({"eating" : "ja", "books" : "nee", "piano" : "coke", "excitement" : "zoo"}), ('ja', 'nee', 'coke', 'zoo'))
