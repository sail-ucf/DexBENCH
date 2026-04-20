import unittest

def f(st, pattern):
    for p in pattern:
        if not st.startswith(p): return False
        st = st[len(p):]
    return True


unittest.TestCase().assertEqual(f('qwbnjrxs', ['jr', 'b', 'r', 'qw']), False)
