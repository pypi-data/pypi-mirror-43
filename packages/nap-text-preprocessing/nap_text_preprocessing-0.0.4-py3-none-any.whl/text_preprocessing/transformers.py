import markovify

import numpy as np
import pandas as pd

from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from pymorphy2 import MorphAnalyzer


class BayesPredictions(TransformerMixin):
    def __init__(self, vectorizer):
        self.unigram_mnb = Pipeline([('text', vectorizer), ('mnb', OneVsRestClassifier(MultinomialNB()))])

    def fit(self, x, y=None):
        self.unigram_mnb.fit(x, y)
        return self
    
    def add_unigram_predictions(self, text_series):
        return self.unigram_mnb.predict_proba(text_series)

    def transform(self, x):
        return self.add_unigram_predictions(x)


class TextLen(TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, x):
        textlen_features = []
        for s in x:
            textlen_features.append([len(s.split())])
        return np.array(textlen_features)


BEGIN = '___BEGIN__'
END = '___END__'


class MarkovChain(TransformerMixin):
    def __init__(self, state_size=1):
        self.state_size = state_size

    def fit(self, x, y=None):
        
        if isinstance(x, pd.Series):
            x = x.values
            
        if isinstance(y, pd.Series):
            y = y.values
        self.models = []
        nonzero = np.nonzero(y)
        for label in range(y.shape[1]):
            samples_inds = nonzero[0][np.where(nonzero[1] == label)]
            label_text = '. '.join([s[0].upper() + s[1:] if len(s) > 1 else s for s in x[samples_inds] ])
            if label_text:
                self.models.append(markovify.Text(label_text, self.state_size).chain.model)
            else:
                self.models.append(dict())
        return self
    
    def transform(self, x):
        if isinstance(x, pd.Series):
            x = x.values
        markov_features = []
        for sentence in x:
            tokens = sentence.split(' ')
            items = ([ BEGIN ] * self.state_size) + tokens + [ END ]
            sample = [0] * len(self.models)
            for i in range(len(tokens) + 1):
                ngram = tuple(items[i:i+self.state_size])
                follow = items[i+self.state_size]
                for ind, model in enumerate(self.models):
                    if ngram in model:
                        sample[ind] += model[ngram].get(follow, 0)
            all_entrance = np.sum(sample)
            if all_entrance:
                sample = sample / all_entrance
            markov_features.append(sample)
        return np.array(markov_features)


class Lemmatizator(TransformerMixin):
    def __init__(self, pymorphy_dict_path='./dict_data/pymorphy2_dicts/data'):
        self.morph = MorphAnalyzer(path=pymorphy_dict_path)
    
    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        lemmas = []
        for doc in x:
            lemmas.append(' '.join([str(self.morph.parse(word)[0].normal_form) for word in doc.split()]))
        return np.array(lemmas)
