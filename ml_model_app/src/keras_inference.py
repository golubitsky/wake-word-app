from tensorflow import keras

MODEL = keras.models.load_model('/app/ml_model_app/models/baseline.h5')


def predict():
    return 'hello world'
