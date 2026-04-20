import unittest

def f(text, separator):
    splitted = text.splitlines()
    if separator:
        return [' '.join(s) for s in splitted]
    else:
        return splitted


unittest.TestCase().assertEqual(f('dga nqdk\rull qcha kl', 1), ['d g a   n q d k', 'u l l   q c h a   k l'])
