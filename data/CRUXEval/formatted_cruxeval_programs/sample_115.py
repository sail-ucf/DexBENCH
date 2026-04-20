import unittest

def f(text):
    res = []
    for ch in text.encode('utf-8'):
        if ch == 61:
            break
        if ch == 0:
            pass
        res.append(f'{ch}; '.encode('utf-8'))
    return b''.join(res)


unittest.TestCase().assertEqual(f('os||agx5'), b'111; 115; 124; 124; 97; 103; 120; 53; ')
