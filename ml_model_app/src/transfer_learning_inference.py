import zipfile
import uuid
import os

from tensorflow import keras
import numpy as np

DEFAULT_PATH_TO_ZIP_FILE = '/app/ml_model_app/models/MNIST_with_transfer_learning.zip'


class Model(object):
    def __init__(self, path_to_zip_file=DEFAULT_PATH_TO_ZIP_FILE):
        self.load_model_from_zip_file(path_to_zip_file)

    def load_model_from_zip_file(self, path_to_zip_file):
        temp_path = f'/tmp/{str(uuid.uuid4())}'

        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_path)
            self.model = keras.models.load_model(os.path.join(temp_path, 'content/mnist_model'))

    def single_predict(self, sample):
        sample_in_higher_rank_tensor = np.expand_dims(sample, axis=0)
        y = self.model.predict(sample_in_higher_rank_tensor)

        return int(np.argmax(y))

    def evaluate(self, x, y, verbose=0):
        # x is a test batch, y is test labels,
        # change verbose if desired
        # not doing size checks here, should check re: formatting and use case
        score = self.model.evaluate(x, y, verbose)
        return score


MODEL = Model()


def predict(sample):
    return MODEL.single_predict(sample)
