from tensorflow import keras
import numpy as np

MODEL = keras.models.load_model('/app/ml_model_app/models/baseline.h5')


def predict(sample):
    # https://stackoverflow.com/a/43019294/3833166
    sample_in_higher_rank_tensor = np.expand_dims(sample, axis=0)
    prediction = MODEL.predict(sample_in_higher_rank_tensor)

    return int(np.argmax(prediction))
