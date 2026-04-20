import unittest

def f(replace, text, hide):
    while hide in text:
        replace += 'ax'
        text = text.replace(hide, replace, 1)
    return text


unittest.TestCase().assertEqual(f('###', "ph>t#A#BiEcDefW#ON#iiNCU", '.'), 'ph>t#A#BiEcDefW#ON#iiNCU')
