from Drive import *
from util import *
import datetime
class myDrive():
    def __init__(self,filenames,driverId):
        self.drives = [Drive("json/"+str(name)+".json") for name in filenames]
        self.driverId = driverId

        speeds,axes,ays,jxes,jys = [],[],[],[],[]

        divax = []
        divay = []
        divsp = []
        divjx = []
        divjy = []

        for d in self.drives:
            # first point check
            prevTime = 0
            #divide acceleration for x direction
            '''
            for i in range(len(d.ax)):
                if (np.abs(d.ax[i]) >5):
                    prevTime = d.ax.index[i]
                    break
            changedPoints = []
            sign = check_sign(d.ax[prevTime])
            # search change point
            for i in d.ax.index:
                prev_sign = sign
                sign = check_sign(d.ax[i])
                if (prev_sign != sign):
                    changedPoints.append(i)
            d.axpoints = changedPoints
            '''
            #divide acceleration for x direction
            prevTime = 0
            for i in range(len(d.ay)):
                if (np.abs(d.ay[i]) >5):
                    prevTime = d.ay.index[i]
                    break
            changedPoints = []
            sign = check_sign(d.ay[prevTime])
            # search change point
            for i in d.ay.index:
                prev_sign = sign
                sign = check_sign(d.ay[i])
                if (prev_sign != sign):
                    changedPoints.append(i)
            d.aypoints = changedPoints

            speeds.append(d.speed)
            axes.append(d.ax)
            ays.append(d.ay)
            jxes.append(d.jx)
            jys.append(d.jy)
            prevTime = d.ax.index[0]
            for p in d.aypoints:
                divax.append(d.ax[prevTime:p-1])
                divay.append(d.ay[prevTime:p-1])
                divsp.append(d.speed[prevTime:p-1])
                divjx.append(d.jx[prevTime:p-1])
                divjy.append(d.jy[prevTime:p-1])
                prevTime = p

        self.divax = divax
        self.divay = divay
        self.divsp = divsp
        self.divjx = divjx
        self.divjy = divjy
        self.axes  = axes
        self.ays  = ays
        self.jxes  = jxes
        self.jys  = jys
        self.speeds  = speeds

    def drivesFromSeries(self,series):
        fromt = series.index[0]
        tot = series.index[-1]
        for d in self.drives:
            if (d.startTime-1 < fromt and d.endTime+1 > tot ):
                return d
        return nil

    def comfortable(self,series):
        d = self.drivesFromSeries(series)
        return d.comfortable(series)

    def rmsSeries(self, series, _type, time=2):
        d = self.drivesFromSeries(series)
        rmsSeries = []
        for index in series.index:
            ser = self.cutSeries(index,d,_type,time)
            rmsSeries.append(rms(ser))
        return pd.Series(rmsSeries,series.index)
    #Seriesの任意の時間前秒のSeriesを切り出す
    def cutSeries(self,_from,d,_type = "ay",time = 2):
        if (_type == "ay"):
            return d.ay[_from-datetime.timedelta(seconds =2) :_from]
        else:
            return nil
