from Drive import *
import numpy as np
def standardization(st):
    import scipy.stats as sp
    st_std = sp.stats.zscore(st, axis=0)
    return st_std

def velocity2mG(velocity):
    return velocity/3600*1000*100*0.101971621
def mG2kmh(mg):
    return mg*3600/1000/100*9.806
def each_corrcoef(ary):
    for i in range(len(ary[0])):
        for j in range(len(ary[0])-i-1):
            print(np.corrcoef(ary[:,i], ary[:,i+j+1])[0,1])
