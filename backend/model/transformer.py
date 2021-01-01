import numpy as np
import pandas as pd
import pickle
import os

# suppress all tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# tensorflow
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
#
from scipy.sparse import csr_matrix

# get path
def get_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

# load embeddings
def load_vectorizer(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

class Model:
    def __init__(self):

        self.veczr = load_vectorizer(get_path('../data/vectorizer.pkl'))
        self.model = load_model(get_path('../data/nn.h5'))
        #
        self.authors = pd.read_csv(get_path('../data/Authors.csv'), index_col='ID')

    # convert text to sparse matrices
    def vectorize(self, arr: list):
        return csr_matrix.sorted_indices(self.veczr.transform(arr))

    # predict labels
    def predict(self, vec):
        return self.model.predict(vec)

    def run(self, text: str):
        prediction = self.predict(self.vectorize(text.split('.')))
        # get mean of all sentences
        prediction = np.mean(prediction, axis=0)
        #
        label, confidence = np.argmax(prediction), np.max(prediction)
        # retrieve name from the label
        author = self.authors.loc[label]['Author']
        img = self.authors.loc[label]['Img']

        return author, np.round(confidence, 2), img