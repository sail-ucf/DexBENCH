import unittest

def f(price, product):
    inventory = ['olives', 'key', 'orange']
    if product not in inventory:
        return price
    else:
        price *=.85
        inventory.remove(product)
    return price


unittest.TestCase().assertEqual(f(8.50, 'grapes'), 8.5)
