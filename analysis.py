from util import *
from sklearn import *
from scipy.spatial.distance  import pdist
from scipy.cluster.hierarchy import dendrogram,ward,leaves_list,average,linkage
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import to_tree

def test_PCA(stat,num):
    pca =decomposition.PCA(n_components = num)
    pca.fit(stat)
    print(np.cumsum(pca.explained_variance_ratio_))
    s_pca = pca.transform(stat)
    return s_pca

def test_dendrogram(st,cutnum=8):
    dis = ward(st)
    h_cls = linkage(dis)
    return dendrogram(h_cls,p=cutnum ,truncate_mode='lastp')
