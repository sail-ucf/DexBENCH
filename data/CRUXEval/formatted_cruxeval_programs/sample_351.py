import unittest

def f(text):
    try:
        while 'nnet lloP' in text:
            text = text.replace('nnet lloP', 'nnet loLp')
    finally:
        return text


unittest.TestCase().assertEqual(f('a_A_b_B3 '), 'a_A_b_B3 ')
