import pandas as pd
from sklearn.cluster import KMeans

class KMeansCluster(object):
    def __init__(vector_column, n_classes=2):
        self.vector_column = vector_column
        self.k_means = KMeans(n_clusters=n_classes)

    def apply(records):
        classes = self.k_means.fit_predict(records[self.vector_column])
        import pdb; pdb.set_trace()
        return
