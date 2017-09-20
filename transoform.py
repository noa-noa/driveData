from personalization import *
def transform(drivers):
    path = "csv/"
    dfs = []
    for dr in drivers:
        drdfs = []
        for d  in dr.drives:
            df = pd.DataFrame()
            df["speed"] = upsamp(d.speed,len(d.speed)*5-4)
            df["ax"] = d.ax
            df["ay"] = d.ay
            df["az"] = d.az
            df["lat"] = upsamp(d.lat,len(d.lat)*5-4)
            df["lon"] = upsamp(d.lon,len(d.lon)*5-4)
            df["dist"]= upsamp(d.dist,len(d.dist)*5-4)
            df["rpm"]= upsamp(d.rpm,len(d.rpm)*5-4)
            df.userId = dr.driverId
            df.filename = d.name
            fname = df.filename.replace("json/","")
            fname = fname.replace(".json","")
            drdfs.append(df)
            df.to_csv(path+fname+".csv")
        dfs.append(drdfs)
if __name__ == "__main__":
    transform(driver)
