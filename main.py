from util import *
import os
import matplotlib.pyplot as plt
import features as ft
import numpy as np
if __name__ != "__main__":
    filenames = os.listdir("json/")
    drivers = [Drive("json/"+str(i)) for i in filenames]
    drives = [[],[]]
    for d in drivers:
        drive = d.divide_drive()
        drives[0]+=drive[0]
        drives[1]+=drive[1]
    f  = ft.features(drives[0])
    division = []
    for d in drivers:
        division+=d.divide_drivings()

    drivegps(drivers)
    
