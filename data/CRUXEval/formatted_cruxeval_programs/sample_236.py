import unittest

def f(array):
    if len(array) == 1:
        return ''.join(array)
    result = list(array)
    i = 0
    while i < len(array)-1:
        for j in range(2):
            result[i*2] = array[i]
            i += 1
    return ''.join(result)


unittest.TestCase().assertEqual(f(['ac8', 'qk6', '9wg']), 'ac8qk6qk6')
