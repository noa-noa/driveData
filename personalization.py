import os
import matplotlib.pyplot as plt
import features as ft
from myDrive import myDrive
from util import *
driver = []
if __name__ != "__main__":
    #filenames = os.listdir("json/")
    detail_df = pd.read_csv("drive_detail.csv")
    ids = detail_df["driverId"].value_counts()
    for i in ids.index:
        filenames = detail_df[detail_df["driverId"] == i]["driveId"]
        d = myDrive(filenames = filenames.values,driverId = i)
        driver.append(d)
