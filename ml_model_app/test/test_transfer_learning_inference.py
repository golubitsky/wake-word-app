import numpy as np

from src.transfer_learning_inference import predict
from src.load_image import read_image_file


def test_predict_interface():
    sample = np.zeros((28, 28, 1))
    assert type(predict(sample)) == int
    assert predict(sample) == 1


def test_model_sanity_check():
    for class_name in range(10):
        for index in range(2):
            path = f'/app/ml_model_app/samples/{class_name}_sample_{index}.png'
            assert predict(read_image_file(path)) == class_name
