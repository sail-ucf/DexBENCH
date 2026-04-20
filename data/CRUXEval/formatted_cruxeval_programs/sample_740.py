import unittest

def f(plot, delin):
    if delin in plot:
        split = plot.index(delin)
        first = plot[:split]
        second = plot[split + 1:]
        return first + second
    else:
        return plot


unittest.TestCase().assertEqual(f([1, 2, 3, 4], 3), [1, 2, 4])
