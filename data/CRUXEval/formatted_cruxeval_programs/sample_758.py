import unittest

def f(nums):
    if nums[::-1] == nums:
        return True
    return False


unittest.TestCase().assertEqual(f([0, 3, 6, 2]), False)
