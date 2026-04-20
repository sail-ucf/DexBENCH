import unittest

def f(arr):
    result = []
    for item in arr:
        try:
            if item.isnumeric():
                result.append(int(item)*2)
        except ValueError:
            result.append(item[::-1])
    return result


unittest.TestCase().assertEqual(f(["91", "16", "\u0661", "5r", "egr", "", "f", "q1f", "三"]), [182, 32])
