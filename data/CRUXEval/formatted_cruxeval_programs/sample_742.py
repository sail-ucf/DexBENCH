import unittest

def f(text):
    b = True
    for x in text:
        if x.isdigit():
            b = True
        else:
            b = False
            break
    return b


unittest.TestCase().assertEqual(f("-1-3"), False)
