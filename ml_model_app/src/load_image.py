
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array


def normalized(image_array):
    return image_array / 255.0


def read_image_file(path):
    image = load_img(path, target_size=(28, 28), color_mode='grayscale')

    return normalized(img_to_array(image))
