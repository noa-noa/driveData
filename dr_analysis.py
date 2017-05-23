import analysis as an
from util import *


def cl_c(dendro):
    cl =dendro["color_list"]
    c = dendro["ivl"]
    c = [int(i) for i in c]
    return cl,c

def tcls(st):
    pcad = an.pdist(st,"Mahalanobis")
    pcl = an.ward(pcad)
    pcadd = an.dendrogram(pcl)
    cl =pcadd["color_list"]
    A = pcadd["ivl"]
    A = [int(i) for i in A]
    return pcadd
def high_low_speed_index(drivers):
    s = speeds(drivers)
    h = []
    l = []
    for i in range(len(s)):
        if s[i] > 20:
            h.append(i)
        else:
            l.append(i)
    return h,l
def speeds(drivers):
    l = []
    for d in drivers:
        start,stop = d.time_division("speed")
        for s in start:
            l.append(s[-1])
    return l
def endpoint(drivers):
    for d in drivers:
        endpoint = []
        for i in d.risingPoints:
            pointIndex=i
            for j in range(len(d.data)- pointIndex):
                if(pointIndex+j+1>=len(d.data)):
                    print("out of index")
                    endpoint.append(pointIndex+j)
                    break
                if (float(d.data[pointIndex+j+1]["speed"])<=0.1):
                    endpoint.append(pointIndex+j+1)
                    break;
        d.endpoint = endpoint
    return drivers

if __name__ != "__main__":
    from main import *
    #f = np.array(f)
    #startd = standardization(f)
    # stop
    #tl=an.linkage(an.pdist(startd),"average")
    #an.dendrogram(tl, p=8, truncate_mode='lastp')
    #br = an.to_tree(tl).get_left().pre_order()
    # start
