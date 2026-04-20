import unittest

def f(st):
    if st[0] == '~':
        e = st.rjust(10, 's')
        return f(e)
    else:
        return st.rjust(10, 'n')


unittest.TestCase().assertEqual(f('eqe-;ew22'), 'neqe-;ew22')
