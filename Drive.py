import json
from pylab import show
import pandas as pd
import shelve
from scipy.interpolate import interp1d
from datetime import datetime as dt
from util import *
class Drive():
    drivers = []
    def __init__(self,filename=None):
        if filename == None:
            return
        f = open(filename,"r")
        json_dict = json.loads(f.read())
        #ax,ay,az,brake,speed,rpm,accel = [],[],[],[],[],[],[]
        ax,ay,az,speed,rpm,distance,latitude,longitude = [],[],[],[],[],[],[],[]
        for js in json_dict:
            #brake.append(js["brake"])
            speed.append(js["speed"])
            rpm.append(js["rpm"])
            distance.append(js["distance"])
            latitude.append(js["latitude"])
            longitude.append(js["longitude"])
            #accel.append(js["accel"])
            for i in range(5):
                ax.append(js["a"+str(i)+"x"])
                ay.append(js["a"+str(i)+"y"])
                az.append(js["a"+str(i)+"z"])
        firsttime = json_dict[0]["time"]
        rng = pd.date_range(dt.fromtimestamp(firsttime),periods=len(ax),freq='200L')
        self.ax = pd.Series(ax,rng)
        self.ay = pd.Series(ay,rng)
        self.az = pd.Series(az,rng)
        rng = pd.date_range(dt.fromtimestamp(firsttime),periods=len(speed),freq='1000L')
        self.name = filename
        self.speed = pd.Series(speed,rng)
        self.dist = pd.Series(distance,rng)
        self.lat = pd.Series(latitude,rng)
        self.lon = pd.Series(longitude,rng)
        #self.brake = pd.Series(brake,rng)
        self.rpm = pd.Series(rpm,rng)
        #self.accel = pd.Series(accel,rng)
        self.sec = 5+1
        #duration time is 5
        self.jx = self.ax.diff()
        self.jy = self.ay.diff()
        self.jz = self.az.diff()
        self.stop_points()
        if (self.start == []):
            return
        firstpoint = self.speed.index[self.start[0]]-1
        endpoint= self.speed.index[self.stop[-1]]+1
        self.speed = self.speed[firstpoint:endpoint]
        self.ax = self.ax[firstpoint:endpoint]
        self.ay = self.ay[firstpoint:endpoint]
        self.az = self.az[firstpoint:endpoint]
        self.dist = self.dist[firstpoint:endpoint]
        self.lat = self.lat[firstpoint:endpoint]
        self.lon = self.lon[firstpoint:endpoint]
        self.rpm = self.rpm[firstpoint:endpoint]

        self.jx = self.jx[firstpoint:endpoint]
        self.jy = self.jy[firstpoint:endpoint]
        self.jz = self.jz[firstpoint:endpoint]

        self.stop_points()

    def stop_points(self):
        zeroPoints =[]
        stop_points = []
        start_points = []
        i = 0
        sec = self.sec
        num = len(self.speed)
        for i in range(num-sec):
            if float(self.speed[i])<=0.1 and 0.0<float(self.speed[i+1]):
                value = self.__zero_transition(i)
                if value:
                    start_points.append(i)
            if float(self.speed[num-i-1])<0.1 and 0.0<float(self.speed[num-i-2]):
                value = self.__zero_transition(num-i-1,-1)
                if value:
                    stop_points.append(num-i-1)
        stop_points.reverse()
        self.start = start_points
        self.stop = stop_points

    def divide_drive(self):
        if (hasattr(self, 'start') == False):
            self.stop_points()
        start = []
        stop = []
        for s in self.start:
            start.append(self.divide_by_index_for_sec(s,1))
        for s in self.stop:
            stop.append(self.divide_by_index_for_sec(s,-1))
        drive = [start,stop]
        return drive
    def divide_drivings(self):
        if (hasattr(self, 'start') == False):
            self.stop_points()
        drives = []

        for i in range(len(self.start)):
            if (i < len(self.stop)):
                drives.append(self.divide_by_index(self.start[i],self.stop[i]))
        return drives
    def calibration(self):
        self.ax -= self.ax[0]
    def __zero_transition(self,index,sign = 1):
        sec = self.sec
        for i in range(sec):
            if 0.1 > float(self.speed[index+(i+1)*sign]):
                return False
#        if float(self.speed[index+(i+1)*sign]) < 0.1:
#            return False
        return True

    def divide_by_index_for_sec(self,start,sign=1):
        sec = self.sec
        if (sign == 1):
            sp = self.speed[start:start+sec*sign]
        else:
            sp = self.speed[start+sec*sign:start]
        st = sp.index[0]
        ax = self.ax[sp.index[0]:sp.index[-1]]
        jx = self.jx[sp.index[0]:sp.index[-1]]
        az = self.az[sp.index[0]:sp.index[-1]]
        jz = self.jz[sp.index[0]:sp.index[-1]]
        ay = self.ay[sp.index[0]:sp.index[-1]]
        jy = self.jy[sp.index[0]:sp.index[-1]]

        return [sp,ax,jx,az,jz,ay,jy]

    def divide_by_index(self,start,stop):
        sp = self.speed[start:stop+1]
        time_start = sp.index[0]
        time_stop = sp.index[-1]
        ax = self.ax[time_start:time_stop]
        jx = self.jx[time_start:time_stop]
        az = self.az[time_start:time_stop]
        jz = self.jz[time_start:time_stop]
        ay = self.ay[time_start:time_stop]
        jy = self.jy[time_start:time_stop]
        return [sp,ax,jx,az,jz,ay,jy]
    def ac_dec(self):
        index = self.search_steady_state()
        ac = []
        for i in range(len(index)-1):
             if ((index[i+1]-index[i]).total_seconds() > 0.2):
                 ac.append(self.ax[index[i]:index[i+1]+1])
        return ac
    def search_steady_state(self):
        index =[]
        for i in range(len(self.speed)-1):
            if (self.speed[i] == self.speed[i+1]):
                index.append(self.speed.index[i+1])
        for i in range(len(self.ax)-1):
            if (self.ax[i] >= 0 and self.ax[i+1] < 0):
                index.append(self.ax.index[i+1])
            elif (self.ax[i] <= 0 and self.ax[i+1] > 0):
                index.append(self.ax.index[i+1])
        list(set(index)).sort()
        return index
