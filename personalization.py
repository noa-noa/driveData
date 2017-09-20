import os
import matplotlib.pyplot as plt
import features as ft
from myDrive import myDrive
from util import *
import re
driver = []
if __name__ != "__main__":
    #filenames = os.listdir("json/")
    '''
    detail_df = pd.read_csv("drive_detail.csv")
    ids = detail_df["driverId"].value_counts()
    for i in ids.index:
        filenames = detail_df[(detail_df["driverId"] == i) & (detail_df["note"] != "bad calibration")]["driveId"]
        d = myDrive(filenames = filenames.values,driverId = i)
        driver.append(d)
    '''
    detail_df = pd.read_csv("drive_detail.csv")

    ids = detail_df["driverId"].value_counts()
    dfs = []
    for i in ids.index:
        filenames = detail_df[(detail_df["driverId"] == i) & (detail_df["note"] != "bad calibration")]["driveId"]
        drdfs = []
        for name in filenames:
             drdfs.append(pd.read_csv("csv/"+re.sub(r'"', '', name)+".csv"))
        dfs.append(drdfs)

'''

ここから切り出し用のコードです.
よくわからないと思うので今度改修します.
'''
term = 90
def beforeStop(df):
    prev = np.nan
    start = []
    stop = []
    justStop = []
    for i in range(len(df.speed)):
        if (math.isnan(prev) != True):
            if(prev != 0 and df.speed[i] == 0):
                if ( df.speed[i+1] == 0):
                    stop.append(i)
                else:
                    justStop.append(i)
        prev = df.speed[i]
    return stop,justStop

def beforeStart(df):
    prev = np.nan
    start = []
    justStart = []
    for i in range(len(df.speed)):
        if (math.isnan(prev) != True):
            if (prev == 0 and df.speed[i]  != 0):
                if (i-2>=0 and df.speed[i-2] == 0):
                    start.append(i)
                else:
                    justStart.append(i)
        prev = df.speed[i]
    return start,justStart

def invertValue(series,df):
    pJrks = []
    prevJrk = np.nan
    t = invertPoint(series,df)
    if( t is None) :
        return None
    return df.jx[t]
def invertPoint(series,df):
    invertPoints = []
    prevJrk = np.nan
    pJrks = []

    for i in range(len(series)):
        if (math.isnan(prevJrk) != True):
            jrk = df.jx[series.index[i]]
            if (prevJrk>0  and  jrk < 0 ):
                invertPoints.append(series.index[i-1])
                pJrks.append(prevJrk)
        prevJrk = df.jx[series.index[i]]
    if ( pJrks == []):
        return None
    else:
        return invertPoints[np.argmax(pJrks)]

def seriesStart(index,df):
    ser = []
    for s in index:
        if(s+term >=len(df.speed)):
            t = df[len(df.speed)-term*2:len(df.speed)].ax
        elif(s-term < 0):
            t = df[0:term*2].ax
        else:
            t = df[s-term:s+term].ax
        ser.append(t)
    return ser

def series(index,df):
    ser = []
    for s in index:
        if(s+term >=len(df.speed)):
            t = df[len(df.speed)-term:len(df.speed)].ax
        elif(s-term < 0):
            t = df[0:term*2].ax
        else:
            t = df[s-term:s+term].ax
        ser.append(t)
    return ser

def seriesStop(index,df):
    ser = []
    for i in index:
        if(i+term >len(df.speed)):
            t = df[len(df.speed)-term:len(df.speed)].ax
        elif(i-term < 0):
            t = df[0:term*2].ax
        else:
            t = df[i-term:i+term-30].ax

        beg = None
        fin = None
        a = t
        for s in range(len(t.index)):
            ind = t.index[s]
            find = i + s
            if (beg is None
                and ind < i
                and df.jx[ind] >=0
                and df.jx[ind+1] <= -50
                and df.ax[ind+1]  <= 10
                and df.speed[ind + 1]>1):
                beg = ind
                a = df.ax[max(beg-1,0):a.index[-1]+1]
            if ( fin is  None
                and  find+1 < t.index[-1]
                and df.jx[find] >=0
                and df.ax[find]  >= -20
                and df.jx[find+1] <=0 ):
                fin = find
                a = df.ax[a.index[0] : fin+1]
            if (find+1 < t.index[-1]  and df.speed[find+1] >=1):
                fin = find
                a = df.ax[a.index[0] : fin+1]
            if (beg is not None and fin is not None):
                ser.append(a)
                break

        ser.append(a)
    return ser

#latG=straight
backSign = -1
fps = 5
def rms(data):
    return math.sqrt((data**2).mean())

def comfortable(df):
    xcomf,ycomf = [],[]
    for i in df["ax"].index:
        xcomf.append(x_comfortable(df,i))
        ycomf.append(y_comfortable(df,i))
    return xcomf,ycomf
def comfortable(df,_from,_to):
    xcomf,ycomf = [],[]
    for df.ax.
def x_comfortable(df,_to):
    Bx1,Bx2,Bx3,Bx4,ex = 0.15, 0.58, 0.20, 0.30, 0.218
    _from = np.max([0,_to-fps*3])
    app = g2ms(df.ax[_from : _to].min())
    apm = g2ms(df.ax[_from : _to].max())
    app = np.abs(app) if app < 0 else 0
    apm = np.abs(apm) if apm > 0 else 0
    j = g2ms(df.jx[_from : _to])
    jrp = 0
    jrm = 0
    if (j.mean() < 0):
        jrp = rms(g2ms(df.jx[_from : _to]))
    else:
        jrm = rms(g2ms(df.jx[_from : _to]))
    return Bx1*app + Bx2*apm +Bx3*jrp + Bx4*jrm + ex

def y_comfortable(df,_to):
    By,Bya,Byj,ex = -0.363, 1.080, 0.125, 0.116
    _from = np.max([0,_to-fps*3])
    arms = rms(g2ms(df.ay[_from : _to]))
    jrms = rms(g2ms(df.jy[_from : _to]))

    return By + Bya*arms + Byj*jrms + ex

def g2ms(value):
    return value*9.80665/1000
