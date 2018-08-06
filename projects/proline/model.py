import os
import logging
import pandas as pd
import numpy as np
import pandas as pd
import tensorflow as tf

from dataland.file_utils import incremental_timestamp
from sklearn.model_selection import train_test_split

INPUT_COLUMNS=['h_plus', 'h', 't', 'v', 'v_plus']
OUTPUT_COLUMNS=['outcome_h_plus', 'outcome_h', 'outcome_t', 'outcome_v', 'outcome_v_plus']

class Train(object):
    def run(self):
        input_train, input_test, output_train, output_test = self.build_train_test_set()
        logging.info('Train size: {}'.format(len(input_train)))
        logging.info('Test size: {}'.format(len(input_test)))

        feature_columns = [
            tf.feature_column.numeric_column('h_plus', dtype=tf.float32),
            tf.feature_column.numeric_column('h', dtype=tf.float32),
            tf.feature_column.numeric_column('t', dtype=tf.float32),
            tf.feature_column.numeric_column('v', dtype=tf.float32),
            tf.feature_column.numeric_column('v_plus', dtype=tf.float32),
        ]

        estimator = self.build_estimator(
            feature_columns,
            OUTPUT_COLUMNS,
            os.path.join('data/proline/models', incremental_timestamp())
        )

        estimator.train(input_fn=tf.estimator.inputs.numpy_input_fn(
            { k: np.array(v) for k, v in input_train[INPUT_COLUMNS].to_dict(orient='list').items() },
            y=output_train[OUTPUT_COLUMNS].astype(np.float32).values,
            num_epochs=100,
            num_threads=1,
            shuffle=True,
        ))

        print estimator.evaluate(input_fn=tf.estimator.inputs.numpy_input_fn(
            { k: np.array(v) for k, v in input_test[INPUT_COLUMNS].to_dict(orient='list').items() },
            y=output_test[OUTPUT_COLUMNS].astype(np.float32).values,
            num_epochs=1,
            num_threads=1,
            shuffle=True,
        ))


    def build_estimator(self, feature_columns, label_values, model_dir):

        def model_fn(features, labels, mode, params):
            label_count = len(params['labels'])

            input_layer = tf.feature_column.input_layer(features, params['feature_columns'])
            output_layer = tf.layers.dense(input_layer, units=label_count)

            loss = tf.nn.sigmoid_cross_entropy_with_logits(
                logits=output_layer,
                labels=labels
            )
            loss = tf.reduce_mean(loss)

            if mode == tf.estimator.ModeKeys.PREDICT:
                predictions = tf.nn.softmax(output_layer)
                probabilities = {}
                for index, item in enumerate(params['labels']):
                    probabilities[item] = predictions[:, index]
                return tf.estimator.EstimatorSpec(mode, predictions=probabilities)
            elif mode == tf.estimator.ModeKeys.TRAIN:
                return tf.estimator.EstimatorSpec(mode, loss=loss,
                    train_op=params['optimizer'].minimize(loss, global_step=tf.train.get_global_step())
                )
            elif mode == tf.estimator.ModeKeys.EVAL:
                predictions = tf.nn.sigmoid(output_layer)
                metrics = {
                    'mean_cosine_distance': tf.metrics.mean_cosine_distance(labels, predictions, 1),
                    'mean_squared_error': tf.metrics.mean_squared_error(labels, predictions),
                    'mean_per_class_accuracy': tf.metrics.mean_per_class_accuracy(labels, tf.round(predictions), label_count)
                }
                return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=metrics)

        return tf.estimator.Estimator(
            model_fn=model_fn,
            model_dir=model_dir,
            params={
                'feature_columns': feature_columns,
                'labels': label_values,
                'optimizer': tf.train.AdamOptimizer(learning_rate=0.1)
        })


    def build_train_test_set(self):
        odds = pd.read_csv('data/proline/odds.csv')
        results = pd.read_csv('data/proline/results.csv')

        results = results[
            (results['outcome_h_plus'] == 1) |
            (results['outcome_h'] == 1) |
            (results['outcome_t'] == 1) |
            (results['outcome_v'] == 1) |
            (results['outcome_v_plus'] == 1)
        ]

        training_set = pd.merge(results, odds, on=['ticket_handle', 'game_handle'], how='left')

        return train_test_split(
            training_set[INPUT_COLUMNS],
            training_set[OUTPUT_COLUMNS],
            test_size = 0.25,
            random_state = 0
        )

if __name__ == '__main__':
    Train().run()
