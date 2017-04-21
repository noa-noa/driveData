import json
from pylab import show
import pandas as pd
import shelve
from scipy.interpolate import interp1d
from datetime import datetime as dt

class Drive():
    drivers = []
    def __init__(self,filename=None):
        if filename == None:
            return
        f = open(filename,"r")
        json_dict = json.loads(f.read())
        #ax,ay,az,brake,speed,rpm,accel = [],[],[],[],[],[],[]
        ax,ay,az,speed,rpm = [],[],[],[],[]
        for js in json_dict:
            #brake.append(js["brake"])
            speed.append(js["speed"])
            rpm.append(js["rpm"])
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
        #self.brake = pd.Series(brake,rng)
        self.rpm = pd.Series(rpm,rng)
        #self.accel = pd.Series(accel,rng)
        self.sec = 5+1
        #duration time is 5
        self.jx = self.ax.diff()
        self.jy = self.ay.diff()
        self.jz = self.az.diff()

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
            start.append(self.__divide_by_index(s,1))
        for s in self.stop:
            stop.append(self.__divide_by_index(s,-1))
        drive = [start,stop]
        return drive
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

    def __divide_by_index(self,start,sign=1):
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
        ay = self.ax[sp.index[0]:sp.index[-1]]
        jy = self.jx[sp.index[0]:sp.index[-1]]
        return [sp,ax,jx,az,jz,ay,jy]
