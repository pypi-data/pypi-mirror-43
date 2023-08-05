import csv
import logging
import os
from threading import Thread

import tensorflow as tf
from tensorflow.python.training.adagrad import AdagradOptimizer
from tensorflow.python.training.adam import AdamOptimizer
from tensorflow.python.training.ftrl import FtrlOptimizer
from tensorflow.python.training.gradient_descent import GradientDescentOptimizer
from tensorflow.python.training.rmsprop import RMSPropOptimizer

logger = logging.getLogger(__name__)


class DeepOCClassifier:

    def __init__(self, workspace, optimizer, hidden_units, learning_rate, train_csv, test_csv, classes, dropout=0.5):
        self.__ws = workspace
        self.__model_dir = os.path.join(workspace)
        self.__optimizer = optimizer
        self.__hidden_units = hidden_units
        self.__train_csv = train_csv
        self.__n_classes = len(classes)
        self.__test_csv = test_csv
        self.__lr = learning_rate
        self.__classes = classes
        self.__train_progress = []
        self.__model = None
        self.__dropout = dropout
        self.__features = self.__get_features(self.__train_csv)

    def __get_features(self, train_csv):
        with open(train_csv, "r") as f:
            reader = csv.reader(f)
            columns_name = next(reader)
            return columns_name

    def __build_model_columns(self, model_columns):
        """

        :type model_columns: list
        """
        model_columns_data = model_columns[:]
        model_columns_data.remove("model")
        model_columns_data.remove("class")
        return [tf.feature_column.numeric_column(k) for k in model_columns_data]

    def __in_memory_input_fn(self, data):

        def decode(x):
            x = tf.split(x, len(self.__features) - 1)
            return dict(zip(self.__features, x))

        dataset = tf.data.Dataset.from_tensor_slices(data)
        iterator = dataset.map(decode).make_one_shot_iterator()
        batch_features = iterator.get_next()
        return batch_features, None

    def __input_fn(self, data_file, header_columns, num_epochs, batch_size, perform_shuffle=False):

        def generate_column_type_default_value(column_types):
            type_defaults = []
            for column in column_types:
                if column == 'model':
                    type_defaults.append([''])
                elif column == 'class':
                    type_defaults.append([0])
                else:
                    type_defaults.append([0.])
            return type_defaults

        def parse_csv(value):
            columns = tf.decode_csv(value, generate_column_type_default_value(header_columns))
            features = dict(zip(header_columns, columns))
            labels = features.pop('class')
            return features, labels
        dataset = tf.data.TextLineDataset(data_file)
        dataset = dataset.skip(1).map(parse_csv, num_parallel_calls=5)
        if perform_shuffle:
            dataset = dataset.shuffle(buffer_size=256)

        dataset = dataset.repeat(num_epochs)
        dataset = dataset.batch(batch_size)
        iterator = dataset.make_one_shot_iterator()
        batch_features, batch_labels = iterator.get_next()
        return batch_features, batch_labels

    def __build_estimator(self, features):
        deep_columns = self.__build_model_columns(features)
        run_config = tf.estimator.RunConfig().replace(
            session_config=tf.ConfigProto(device_count={'GPU': 0}))
        optimizer = AdagradOptimizer(self.__lr)
        if self.__optimizer == "Adam":
            optimizer = AdamOptimizer(self.__lr)
        if self.__optimizer == "Ftrl":
            optimizer = FtrlOptimizer(self.__lr)
        if self.__optimizer == "RMSProp":
            optimizer = RMSPropOptimizer(self.__lr)
        if self.__optimizer == "GD":
            optimizer = GradientDescentOptimizer(self.__lr)
        return tf.estimator.DNNClassifier(
            model_dir=self.__ws,
            feature_columns=deep_columns,
            hidden_units=self.__hidden_units,
            n_classes=self.__n_classes,
            optimizer=optimizer,
            dropout=self.__dropout,
            config=run_config)

    def __train_dll(self, total_epoch, val_per_n_epochs, batch_size, inf_loss_decreasing):
        headers = self.__features
        self.__model = self.__build_estimator(headers)
        total_rounds = total_epoch // val_per_n_epochs
        mile_stone = 100000
        n = 0
        while n < total_rounds:
            epoch = (n + 1) * val_per_n_epochs
            self.__model.train(input_fn=lambda: self.__input_fn(
                self.__train_csv, headers, val_per_n_epochs, batch_size, True))
            result = self.__model.evaluate(input_fn=lambda: self.__input_fn(self.__test_csv, headers, 1, batch_size))
            logger.info("epoch %d, %s", epoch, result)
            previous_loss = result['average_loss']
            if inf_loss_decreasing and n == total_rounds - 1 and mile_stone > previous_loss + 0.05:
                total_rounds += 100
                mile_stone = previous_loss
            n += 1
            self.__train_progress.append({'epoch': epoch, **result})

    def train_dll_model(self, total_epoch, epochs_per_test, batch_size, background=False, inf_loss_decreasing=False):
        thread = Thread(target=self.__train_dll, args=(total_epoch, epochs_per_test, batch_size, inf_loss_decreasing))
        thread.start()
        if not background:
            thread.join()

    def report_progress(self):
        return self.__train_progress

    def predict(self, scores):
        if 'model' in scores:
            scores['model'] = 0
        ontology_scores = [float(scores[key]) for key in self.__features if key not in ['class']]
        if self.__model is None:
            self.__model = self.__build_estimator(self.__features)
        predict_result = list(self.__model.predict(input_fn=lambda: self.__in_memory_input_fn([ontology_scores])))
        return predict_result

