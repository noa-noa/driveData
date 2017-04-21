import init
import analysis as an
import plots as pls
import features as ft
from model_util import *

def evaluation(drivers,index):
    d = index_driver(drivers,index)
    i = index - d.st_index[0]
    dt = dt_influence(d,i)
    return sum(dt)
def allaccels(drivers):
    accels = []
    speeds = []
    rng = pd.date_range('0:00',periods=plotNum,freq='200L')
    for d in drivers:
        i=0
        while i < len(d.data)-sampleNum:
            if judgement_transition_forward(d.data,i):
                accels.append(pd.Series([d.data[i+j]["ax"] for j in range(sampleNum)],rng))
                speeds.append(pd.Series([d.data[i+j]["speed"] for j in range(sampleNum)],rng))
                i=i+sampleNum
            else:
                i=i+1
    return accels,speeds
def cl_c(dendro):
    cl =dendro["color_list"]
    c = dendro["ivl"]
    c = [int(i) for i in c]
    return cl,c

def separatecolor(link,dendro):
    cl = dendro["color_list"]
    leafnum = len(dendro["leaves"])
    dic = dict()
    print(leafnum)
    for i in range(len(link)):
        if(int(link[i][0])<leafnum):
            if str(int(link[i][0])) not in dic:
                dic.update({str(int(link[i][0])):cl[i]})
        if(int(link[i][1])<leafnum):
            if str(int(link[i][1])) not in dic:
                dic.update({str(int(link[i][1])):cl[i]})
    return dic
def links(link):
    dic = dict()
    for i in link:
        dic.update({str(int(i[3])):[i[0],i[1]]})
    return dic
def pl2dc(cl,st):
    for i in range(len(st)):
        plt.scatter(st[i][0],st[i][1],color=cl[str(i)])
def judgement_transition_forward(data,index):
    ax = data[index]["ax"]
    for i in range(sampleNum):
        if 0.0 >= float(data[index+i+1]["ax"]):
            return False
    return True
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
def self_init():
    drivers = init.driverInfos()
    #sp,ac,js,drivers = ft.initFt(drivers)
    #st = ft.Ft(ac,js)
    stop,stop_drivers = ft.features_stop(drivers)
    start,start_drivers = ft.features_start(drivers)
    #drivers = endpoint(drivers)
    #std_start = standardization(st_start)
    return stop,stop_drivers,start,start_drivers

if __name__ == "__main__":
    drivers,start,startd = self_init()
    c = an.test_kmeans(startd,8)
    an.each_corrcoef(np.array(start))
    pcs = an.test_PCA(startd,4)
    dist = an.pdist(startd,"Mahalanobis")
    h_cls = an.ward(dist)
    an.dendrogram(h_cls)
    show()
else:
    stop,d_stop,start,d_start = self_init()
    stop = np.array(stop)
    start = np.array(start)
    stopd = standardization(stop)
    startd = standardization(start)
    # stop
    tl=an.linkage(an.pdist(stopd),"average")
    an.dendrogram(tl, p=8, truncate_mode='lastp')
    br = an.to_tree(tl).get_left().pre_order()
    # start

    #[plt.scatter(i[0],i[5],color="r") for i in start]
    #[plt.scatter(st[br[i]][0],st[br[i]][5],color="g") for i in range(len(br))]
    #drivers,start,startd = self_init()
    #c = an.test_kmeans(startd,8)
    #an.each_corrcoef(np.array(start))
    #pcs = an.test_PCA(startd,2)
"""
tl=an.linkage(an.pdist(startd),"average")
an.dendrogram(tl, p=8, truncate_mode='lastp')
br = an.to_tree(tl).get_left().pre_order()
#stop
[plt.scatter(i[4],i[3],color="r",s=60) for i in stop]
[plt.scatter(stop[br[i]][4],stop[br[i]][3],color="g",s=60) for i in range(len(br))]
pylab.ylabel("加速度の最大値 [mG]")
pylab.xlabel("加速度の最小値 [mG]")
plt.savefig("stop_amax_amin_euc.pdf")

[plt.scatter(i[-1],i[-2],color="r",s=60) for i in stop]
[plt.scatter(stop[br[i]][-1],stop[br[i]][-2],color="g",s=60) for i in range(len(br))]
pylab.ylabel("ジャークの最大値 [mG/s]")
pylab.xlabel("ジャークの最小値 [mG/s]")
plt.savefig("stop_jmax_jmin_euc.pdf")

[plt.scatter(i[0],i[5],color="r",s=60) for i in stop]
[plt.scatter(stop[br[i]][0],stop[br[i]][5],color="g",s=60) for i in range(len(br))]
pylab.ylabel("ジャークの実効値 [mG/s]")
pylab.xlabel("加速度の実効値 [mG]")
plt.savefig("stop_jrms_arms_euc.pdf")
show()

[plt.scatter(i[1],i[6],color="r",s=60) for i in stop]
[plt.scatter(stop[br[i]][1],stop[br[i]][6],color="g",s=60) for i in range(len(br))]
pylab.ylabel("ジャークの平均値 [mG/s]")
pylab.xlabel("加速度の平均値 [mG]")
plt.savefig("stop_jmean_amean_euc.pdf")
show()

#start
[plt.scatter(i[4],i[3],color="r",s=60) for i in start]
[plt.scatter(start[br[i]][4],start[br[i]][3],color="g",s=60) for i in range(len(br))]
pylab.ylabel("amax [mG]")
pylab.xlabel("amin [mG]")
plt.savefig("start_amax_amin_euc.pdf")
show()

[plt.scatter(i[-1],i[-2],color="r",s=60) for i in start]
[plt.scatter(start[br[i]][-1],start[br[i]][-2],color="g",s=60) for i in range(len(br))]
pylab.ylabel("jmax [mG/s]")
pylab.xlabel("jmin [mG/s]")
plt.savefig("start_jmax_jmin_euc.pdf")
show()

[plt.scatter(i[0],i[5],color="r",s=60) for i in start]
[plt.scatter(start[br[i]][0],start[br[i]][5],color="g",s=60) for i in range(len(br))]
pylab.ylabel("jrms [mG/s]")
pylab.xlabel("arms [mG]")
plt.savefig("start_jrms_arms_euc.pdf")
show()

[plt.scatter(i[1],i[6],color="r",s=60) for i in start]
[plt.scatter(start[br[i]][1],start[br[i]][6],color="g",s=60) for i in range(len(br))]
pylab.ylabel("jmean [mG/s]")
pylab.xlabel("amean [mG]")
plt.savefig("start_jmean_amean_euc.pdf")
show()

"""
