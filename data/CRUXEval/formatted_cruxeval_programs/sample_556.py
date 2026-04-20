import unittest

def f(text):
    for i in range(len(text)):
        if text[i] == ' ':
            text = text.replace(' ', '\t', 1)
    return text.expandtabs(4)


unittest.TestCase().assertEqual(f('\n\n\t\tz\td\ng\n\t\t\te'), '\n\n        z   d\ng\n            e')
