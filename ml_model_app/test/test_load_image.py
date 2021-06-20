import numpy as np

from src.load_image import read_image_file


def test_predict_actual_sample():
    path = '/app/ml_model_app/samples/4_sample_1.png'
    image = read_image_file(path)
    assert image.shape == (28, 28, 1)
    assert np.max(image) == 1
