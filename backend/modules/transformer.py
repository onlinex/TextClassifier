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

        # how many tokens are needed for a sentence to be considered complete
        self.min_num_tokens = 5

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
        stop_list = [' ', '/', '^', '{', '}', '$', '*', '®', '•', '&', '\\', '■', '°']
        # generator to list
        docs = list(docs.sents)
        size = len(docs)
        # allocate memory
        Xs = np.zeros(shape=(size, seq_length, 300), dtype='float32')
        # iterate sentences
        for i, doc in enumerate(docs):
            j = 0
            for token in doc[:seq_length]:
                if token.text in stop_list:
                    continue
                # get index from int64 hash
                Xs[i, j] = token.vector if token.has_vector else self.nlp.vocab[0].vector
                j += 1
                
        return Xs

    # make prediciton less steep
    def smooth(self, p):
        return p ** 0.5 / (np.max(p ** 0.5) / np.max(p))

    # adjust for number of words
    def adjustment_coeff(self, v):
        # number of tokens in each sequence
        num_tokens = np.sum(~np.equal(v[:, :, 0], 0.0), axis=1)
        # calculate coefficients
        coeff = np.min([num_tokens / self.min_num_tokens, np.ones(len(num_tokens))], axis=0)
        return np.reshape(coeff, (-1,1,1))

    def predict_author(self, v):
        # get coefficient to scale down the predictions
        adj_coeff = self.adjustment_coeff(v)
        # predict, avg across sentences
        prediction = np.mean(self.nn_authors.predict(v) * adj_coeff, axis=0)
        
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
        # return None template if input is None
        if np.sum(vectors) == 0:
            return self.get_zero_pattern()
        # Author
        author, confidence, img = self.predict_author(vectors)
        # Genre
        genres = self.predict_genre(vectors)
        # Period
        periods = self.predict_period(vectors)

        return author, confidence, img, genres, periods

    def get_zero_pattern(self):
        author = 'Author unknown'
        confidence = 0.0,
        img = 'http://notio.ink/img/icon1/icon_bordered.png'
        genres = dict(zip(self.genres_names, np.zeros(len(self.genres_names)).astype(str)))
        periods = dict(zip(self.periods_names, np.zeros(len(self.periods_names)).astype(str)))

        return author, confidence, img, genres, periods

