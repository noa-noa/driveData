import json
from pylab import show
import pandas as pd
import shelve
from scipy.interpolate import interp1d
from datetime import datetime as dt

class Drive:
    def __init__(self,filename=None):
        if filename == None:
            return
        f = open(filename,"r")
        json_dict = json.loads(f.read())
        ax,ay,az,brake,speed,rpm,accel = [],[],[],[],[],[],[]
        for js in json_dict:
            brake.append(js["brake"])
            speed.append(js["speed"])
            rpm.append(js["rpm"])
            accel.append(js["accel"])
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
        self.brake = pd.Series(brake,rng)
        self.rpm = pd.Series(rpm,rng)
        self.accel = pd.Series(accel,rng)
        self.sec = 5

    def stop_points(self):
        zeroPoints =[]
        stop_points = []
        start_points = []
        i = 0
        sec = self.sec
        num = len(self.speed)
        for i in range(num-sec):
            if float(self.speed[i])<=0.0 and 0.0<float(self.speed[i+1]):
                value = self.zero_transition(i)
                if value:
                    start_points.append(i)
            if float(self.speed[num-i-1])<=0.0 and 0.0<float(self.speed[num-i-2]):
                value = self.zero_transition(num-i-1,-1)
                if value:
                    stop_points.append(num-i-1)
        stop_points.reverse()
        self.start_points = start_points
        self.stop_points = stop_points
        print(self.start_points)
        print(self.stop_points)

    def zero_transition(self,index,sign = 1):
        sec = self.sec
        for i in range(sec):
            if 0.1 >= float(self.speed[index+(i+1)*sign]):
                return False
        if float(self.speed[index+(i+1)*sign]) < 0.1:
            return False
        return True
