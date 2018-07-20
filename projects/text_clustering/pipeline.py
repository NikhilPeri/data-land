import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.cluster import KMeans

MODEL_SOURCE = 'https://tfhub.dev/google/nnlm-en-dim50-with-normalization/1'

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
    def __init__(self, vector_column, n_classes=2):
        self.vector_column = vector_column
        self.k_means = KMeans(n_clusters=n_classes)

    def apply(self, records):
        classes = self.k_means.fit_predict(np.array(records[self.vector_column].tolist()))
        records['class'] = classes
        return records.sort_values('class')

input = []
with open('projects/text_clustering/data/all/partner/sentences.csv') as text_file:
    for scentence in text_file:
        clean_sentence = scentence.rstrip().lower()
        if clean_sentence not in input:
            input.append(clean_sentence)

print "read {} scentence".format(len(input))
output = VecotirizeSentences().apply(input)
# 8 classes for partners
# 2 classes for merchant
# all partner 10
output = KMeansCluster('vectors', n_classes=11).apply(output)
output.drop('vectors', axis=1).to_csv('projects/text_clustering/data/all/partner/clustered_sentences.csv', index=False)
