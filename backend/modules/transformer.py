import numpy as np
import pandas as pd
import pickle
import os

# suppress all tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# tensorflow
import tensorflow as tf
#
import spacy

# get path
def get_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

# load embeddings
def load_pickle(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

class Model:
    def __init__(self):

        # import spacy to use GloVe vectors
        self.nlp = spacy.load("en_core_web_md")
        self.nlp.max_length = 10e8

        self.nn_authors = tf.keras.models.load_model(get_path('../data/nn_authors.h5'))
        self.nn_genres = tf.keras.models.load_model(get_path('../data/nn_genres.h5'))
        self.nn_periods = tf.keras.models.load_model(get_path('../data/nn_periods.h5'))
        #
        self.authors = pd.read_csv(get_path('../data/Authors.csv'), index_col='ID')
        
        #
        self.genres_names = ['Adventure', 'Crime', 'Fantasy', 'Fiction', 'Novel', 'Satire', 'Science']
        self.periods_names = ['Unknown', 'Renaissance', 'Enlightenment', 'Victorian', 'Modernism', 'Post-modernism']

    # clean text
    def clean(self, text: str):
        # remove digits
        text = ''.join(i for i in text if not i.isdigit())

        return text

    # convert to vectors
    def vectorize(self, docs, seq_length=35):
        # generator to list
        docs = list(docs.sents)
        size = len(docs)
        # allocate memory
        Xs = np.zeros(shape=(size, seq_length, 300), dtype='float32')
        # iterate sentences
        for i, doc in enumerate(docs):
            for j, token in enumerate(doc[:seq_length]):
                # get index from int64 hash
                Xs[i, j] = token.vector if token.has_vector else self.nlp.vocab[0].vector
        return Xs

    def smooth(self, p):
        return p ** 0.5 / (np.max(p ** 0.5) / np.max(p))

    def predict_author(self, v):
        # predict, avg across sentences
        prediction = np.mean(self.nn_authors.predict(v), axis=0)
        
        label, confidence = np.argmax(prediction), np.max(prediction)
        # get data from csv
        name, img = self.authors.loc[label]['Author'], self.authors.loc[label]['Img']
        # return
        return name, np.round(confidence, 2), img

    def predict_genre(self, v):
        # predict, avg across sentences
        prediction = self.smooth(np.mean(self.nn_genres.predict(v), axis=0))
        # return a dictionary
        return dict(zip(self.genres_names, np.round(prediction, 2).astype(str)))

    def predict_period(self, v):
        # predict, avg across sentences
        prediction = self.smooth(np.mean(self.nn_periods.predict(v), axis=0))
        # return a dictionary
        return dict(zip(self.periods_names, np.round(prediction, 2).astype(str)))

    def run(self, text: str):
        # vectorize
        vectors = self.vectorize(self.nlp(text))
        # Author
        author, confidence, img = self.predict_author(vectors)
        # Genre
        genres = self.predict_genre(vectors)
        # Period
        periods = self.predict_period(vectors)

        return author, confidence, img, genres, periods