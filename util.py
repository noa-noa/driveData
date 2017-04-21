from Drive import *

def standardization(st):
    import scipy.stats as sp
    st_std = sp.stats.zscore(st, axis=0)
    return st_std
