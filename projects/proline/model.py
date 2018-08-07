import os
import logging
import pandas as pd
import numpy as np
import pandas as pd
import tensorflow as tf

from dataland.scheduler import Operation
from dataland.file_utils import incremental_timestamp, latest_subdirectory
from sklearn.model_selection import train_test_split

INPUT_COLUMNS=['sport', 'h_plus', 'h', 't', 'v', 'v_plus']
OUTPUT_COLUMNS=['outcome_h_plus', 'outcome_h', 'outcome_t', 'outcome_v', 'outcome_v_plus']

class Train(Operation):
    def perform(self):
        input_train, input_test, output_train, output_test = self.build_train_test_set()
        logging.info('Train size: {}'.format(len(input_train)))
        logging.info('Test size: {}'.format(len(input_test)))

        feature_columns = [
            tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list('sport', input_train.sport.unique())),
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
            shuffle=False,
        ))

        print estimator.evaluate(input_fn=tf.estimator.inputs.numpy_input_fn(
            { k: np.array(v) for k, v in input_test[INPUT_COLUMNS].to_dict(orient='list').items() },
            y=output_test[OUTPUT_COLUMNS].astype(np.float32).values,
            num_epochs=1,
            num_threads=1,
            shuffle=False,
        ))

        model_dir = estimator.export_savedmodel(
            estimator.model_dir,
            tf.estimator.export.build_raw_serving_input_receiver_fn({
                'sport': tf.placeholder(shape=[None, 1], dtype=tf.string),
                'h_plus': tf.placeholder(shape=[None, 1], dtype=tf.float32),
                'h': tf.placeholder(shape=[None, 1], dtype=tf.float32),
                't': tf.placeholder(shape=[None, 1], dtype=tf.float32),
                'v': tf.placeholder(shape=[None, 1], dtype=tf.float32),
                'v_plus': tf.placeholder(shape=[None, 1], dtype=tf.float32),
            })
        )
        os.rename(model_dir, os.path.join(estimator.model_dir, 'export'))

    def build_estimator(self, feature_columns, label_values, model_dir):

        def model_fn(features, labels, mode, params):
            label_count = len(params['labels'])

            input_layer = tf.feature_column.input_layer(features, params['feature_columns'])
            output_layer = tf.layers.dense(input_layer, units=label_count, kernel_regularizer=tf.nn.l2_loss)
            predictions = tf.nn.sigmoid(output_layer)

            if mode == tf.estimator.ModeKeys.PREDICT:
                probabilities = {}
                for index, item in enumerate(params['labels']):
                    probabilities[item] = predictions[:, index]

                serving_output = {
                    'predict': tf.estimator.export.PredictOutput(probabilities)
                }
                return tf.estimator.EstimatorSpec(mode, predictions=probabilities, export_outputs=serving_output)
            elif mode == tf.estimator.ModeKeys.TRAIN:
                loss = tf.nn.sigmoid_cross_entropy_with_logits(
                    logits=output_layer,
                    labels=labels
                )
                loss = tf.reduce_sum(loss)
                return tf.estimator.EstimatorSpec(mode, loss=loss,
                    train_op=params['optimizer'].minimize(loss, global_step=tf.train.get_global_step())
                )
            elif mode == tf.estimator.ModeKeys.EVAL:
                loss = tf.nn.sigmoid_cross_entropy_with_logits(
                    logits=output_layer,
                    labels=labels
                )
                loss = tf.reduce_sum(loss)
                ACTIVATION_THRESHOLDS = [0.5, 0.6, 0.7, 0.8, 0.9]
                metrics = {
                    'mean_cosine_distance': tf.metrics.mean_cosine_distance(labels, predictions, 1),
                    'mean_squared_error': tf.metrics.mean_squared_error(labels, predictions),
                    'mean_per_class_accuracy': tf.metrics.mean_per_class_accuracy(labels, tf.round(predictions), label_count),
                    'precision_at_threshold': tf.metrics.precision_at_thresholds(labels, predictions, ACTIVATION_THRESHOLDS),
                    'recall_at_threshold': tf.metrics.recall_at_thresholds(labels, predictions, ACTIVATION_THRESHOLDS),
                }
                return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=metrics)

        return tf.estimator.Estimator(
            model_fn=model_fn,
            model_dir=model_dir,
            params={
                'feature_columns': feature_columns,
                'labels': label_values,
                'optimizer': tf.train.AdamOptimizer()
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
            test_size = 0.3,
            random_state = 0,
            shuffle=True
        )

class Predict(Operation):
    def perform(self):
        odds = pd.read_csv('data/proline/odds.csv')
        odds = odds[odds['cutoff_date'] > str(pd.Timestamp.now())]

        predicted_outcomes = None
        with tf.Session() as sess:
            prediction_instances = { k: map(lambda x: v) for k, v in odds[INPUT_COLUMNS].to_dict(orient='list').items() }
            predictor = tf.contrib.predictor.from_saved_model(os.path.join(latest_subdirectory('data/proline/models'), 'export'))

            predicted_outcomes = predictor(prediction_instances)

        import pdb; pdb.set_trace()

if __name__ == '__main__':
    Train().perform()
    Predict().perform()
