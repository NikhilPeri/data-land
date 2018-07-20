import math

import pandas as pd
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub

from sklearn.cluster import KMeans

MODEL_SOURCE = 'https://tfhub.dev/google/universal-sentence-encoder/2'

class VecotirizeSentences(object):
    def apply(self, scentences):
        vectors = None

        with tf.Graph().as_default():
            embed = hub.Module(MODEL_SOURCE)
            embeddings = embed(scentences)
            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                sess.run(tf.tables_initializer())

                vectors = sess.run(embeddings)

        return pd.DataFrame({'scentences': scentences, 'vectors': list(vectors) })

class KMeansCluster(object):
    def __init__(self, vector_column, max_classes=20):
        self.vector_column = vector_column
        self.max_classes = max_classes

    def apply(self, records):
        data = np.array(records[self.vector_column].tolist())
        scored_classes = np.zeros(self.max_classes)
        for classes in range(self.max_classes):
            k_means = KMeans(n_clusters=(classes+1))
            k_means.fit(data)
            scored_classes[classes] = math.fabs(k_means.score(data) / (classes+1)**4)

        selected_classes = np.argmin(np.gradient(scored_classes))
        print scored_classes
        print "Using {} classes".format(selected_classes)


        k_means = KMeans(n_clusters=(selected_classes+1))
        records['class'] = k_means.fit_predict(data)
        return records.sort_values('class')
