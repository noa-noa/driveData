def features(drives):
    f = []
    for d in drives:
        f.append(x_feature(d))
    return f


def x_feature(d):
    return [d[1].max(),d[1].min(),d[1].mean(),d[1].std(),d[2].max(),d[2].min(),d[2].mean(),d[2].std()]

#def feature(driver):
