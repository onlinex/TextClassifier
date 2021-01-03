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
from sklearn.preprocessing import Normalizer
#
from scipy.sparse import csr_matrix
from scipy.spatial import distance
#
from spacy.lang.en import English

# get path
def get_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

# load embeddings
def load_pickle(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

class Model:
    def __init__(self):

        self.veczr = load_pickle(get_path('../data/vectorizer.pkl'))
        self.model = load_model(get_path('../data/nn.h5'))
        #
        self.authors = pd.read_csv(get_path('../data/Authors.csv'), index_col='ID')

        # spacy
        self.nlp = English()
        self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))
        self.nlp.max_length = 10e8

        # Singular value decomposition
        self.tsvd = load_pickle(get_path('../data/decomposition.pkl'))
        # kmeans
        self.kmeans = load_pickle(get_path('../data/kmeans.pkl'))


    # clean text and split by sentences
    def clean(self, text: str):
        # remove digits
        text = ''.join(i for i in text if not i.isdigit())
        # convert to sentences
        sentences = np.array([sent.text for sent in self.nlp(text).sents])
        # ensure type
        return [str(s) for s in sentences]

    # convert text to sparse matrices
    def vectorize(self, arr: list):
        return csr_matrix.sorted_indices(self.veczr.transform(arr))

    # predict labels
    def predict(self, vec):
        return self.model.predict(vec)

    def get_style(self, vec):
        # decompose and get mean
        vector = np.mean(self.tsvd.transform(vec), axis=0)

        cluster_centers = self.kmeans.cluster_centers_
        text_styles = [distance.euclidean(center, vector) for center in cluster_centers]

        # normalize vector
        text_styles = Normalizer(norm='l2').transform([text_styles])[0]

        # define style names
        style_names = ['Novel', 'Drama', 'Philosophy']

        return dict(zip(style_names, text_styles))


    def run(self, text: str):
        # vectorize
        vectors = self.vectorize(self.clean(text))
        # prediction
        prediction = np.mean(self.predict(vectors), axis=0)
        #
        label, confidence = np.argmax(prediction), np.max(prediction)
        # retrieve name from the label
        author = self.authors.loc[label]['Author']
        img = self.authors.loc[label]['Img']

        #
        style = self.get_style(vectors)

        return author, np.round(confidence, 2), img, style