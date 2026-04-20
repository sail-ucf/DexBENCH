import unittest

def f(nums, verdict):
    res = [x for x in nums if x != 0]
    result = [[x, verdict(x)] for x in res]
    if result:
        return result
    return 'error - no numbers or all zeros!'


unittest.TestCase().assertEqual(f([0, 3, 0, 1], lambda x: x < 2), [[3, False], [1, True]])
