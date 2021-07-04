# -*- coding: utf-8 -*-
from keras.models import load_model
import numpy as np
import tensorflow as tf

class Model(object):
    def __init__(self, path):
        self.model_path = path # path to UNZIPPED model folder
        
    def load(self):
        self.model = load_model(self.model_path)
        return
    
    def single_predict(self, x): # x is a single input image
        x = x.reshape(1,28,28,1)
        x = x.astype('float32')
        x /= 255
        y = self.model.predict(x)
        return np.argmax(y)
    
    def evaluate(self, x, y, verbose=0): # x is a test batch, y is test labels,
                                         #change verbose if desired
        # not doing size checks here, should check with mischa on
        # formatting and use case
        score = self.model.evaluate(x, y, verbose)
        return score
    
if __name__ == "__main__":
    Model('/Users/georgia/Downloads/content/mnist_model')
    

        