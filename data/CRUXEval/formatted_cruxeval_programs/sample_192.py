import unittest

def f(text, suffix):
    output = text
    while text.endswith(suffix):
        output = text[:-len(suffix)]
        text = output
    return output


unittest.TestCase().assertEqual(f('!klcd!ma:ri', '!'), '!klcd!ma:ri')
