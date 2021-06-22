import uuid
import os
from contextlib import contextmanager

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array


def normalized(image_array):
    return image_array / 255.0


def read_image_file(path):
    image = load_img(path, target_size=(28, 28), color_mode='grayscale')

    return normalized(img_to_array(image))


@contextmanager
def image_from_html_form(file_storage):
    """
    Accepts a werkzeug.datastructures.FileStorage file
    """
    # To leverage tensorflow.keras.preprocessing.image.load_img, write to disk.
    temp_path = f'/tmp/{str(uuid.uuid4())}'
    file_storage.save(temp_path)

    yield read_image_file(temp_path)

    os.remove(temp_path)
