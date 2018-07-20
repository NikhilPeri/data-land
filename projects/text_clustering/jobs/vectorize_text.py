import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub

MODEL_SOURCE = 'https://tfhub.dev/google/nnlm-en-dim50-with-normalization/1'

class VecotirizeSentences(object):
    def apply(self, scentences):
        with tf.Graph().as_default():
          embed = hub.Module(MODEL_SOURCE)
          embeddings = embed(scentences['sentence'])
          with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            sess.run(tf.tables_initializer())

            vectors = sess.run(embeddings)
            import pdb; pdb.set_trace()
