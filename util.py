from Drive import *
import numpy as np
from math import sin, cos, acos, radians

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

def latlng_to_xyz(lat, lng):
    rlat, rlng = radians(lat), radians(lng)
    coslat = cos(rlat)
    return coslat*cos(rlng), coslat*sin(rlng), sin(rlat)

def dist_on_sphere(pos0, pos1, radious=6378.137):
    xyz0, xyz1 = latlng_to_xyz(*pos0), latlng_to_xyz(*pos1)
    sm = sum(x*y for x, y in zip(xyz0, xyz1))
    if (sm > 1.0 or sm == 0.0):
        return 0.0
    return acos(sm)*radious
def drivegps(drivers):
    distGps = []
    for d in drivers:
        rng = pd.date_range(d.lat.index[0],periods=len(d.lat)-1,freq='1000L')
        distGps.append(pd.Series(gps2dist(d.lat.values,d.lon.values),rng))
    return distGps
def gps2dist(lat,lon):
    dist = []
    for i in range(len(lat)-1):
        typ = type("")
        if (type(lat[i+1]) == typ or type(lon[i+1]) == typ or type(lat[i]) == typ or type(lon[i]) == typ ):
            dist.append(0.0)
            continue
        pos0 = float(lat[i]),float(lon[i])
        pos1 = float(lat[i+1]),float(lon[i+1])
        if (lat[i] == lat[i+1] and lon[i] == lon[i+1]):
            dist.append(float(0.0))
        else:
            dist.append(dist_on_sphere(pos0,pos1))
    return dist
