# corpus.learn
# Machine learning for the corpus with Scikit-Learn.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 25 17:23:50 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: learn.py [3100e46] benjamin@bengfort.com $

"""
Machine learning for the corpus with Scikit-Learn.
"""

##########################################################################
## Imports
##########################################################################

import nltk
import unicodedata

from nltk.corpus import wordnet as wn
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.model_selection import KFold
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import precision_recall_fscore_support

from partisan.utils import identity, timeit
from collections import Counter, defaultdict


##########################################################################
## Corpus Loader (Not a transformer)
##########################################################################

class CorpusLoader(object):
    """
    The corpus loader knows how to deal with an NLTK corpus at the top of a
    pipeline by simply taking as input a corpus to read from. It exposes both
    the data and the labels and can be set up to do cross-validation.

    If a number of folds is passed in for cross-validation, then the loader
    is smart about how to access data for train/test splits. Otherwise it will
    simply yield all documents in the corpus.
    """

    def __init__(self, corpus, folds=None, shuffle=True):
        self.n_docs = len(corpus.fileids())
        self.corpus = corpus
        self.folds  = folds

        if folds is not None:
            # Generate the KFold cross validation for the loader.
            self.folds = KFold(self.n_docs, folds, shuffle)

    @property
    def n_folds(self):
        """
        Returns the number of folds if it exists; 0 otherwise.
        """
        if self.folds is None: return 0
        return self.folds.n_folds

    def fileids(self, fold=None, train=False, test=False):
        """
        Returns a listing of the documents filtering to retreive specific
        data from the folds/splits. If no fold, train, or test is specified
        then the method will return all fileids.

        If a fold is specified (should be an integer between 0 and folds),
        then the loader will return documents from that fold. Further, train
        or test must be specified to split the fold correctly.
        """
        if fold is None:
            # If no fold is specified, return all the fileids.
            return self.corpus.fileids()

        # Otherwise, identify the fold specifically and get the train/test idx
        for fold_idx, (train_idx, test_idx) in enumerate(self.folds):
            if fold_idx == fold: break
        else:
            # We have discovered no correct fold.
            raise ValueError(
                "{} is not a fold, specify an integer less than {}".format(
                    fold, self.folds.n_folds
                )
            )

        # Now determine if we're in train or test mode.
        if not (test or train) or (test and train):
            raise ValueError(
                "Please specify either train or test flag"
            )

        # Select only the indices to filter upon.
        indices = train_idx if train else test_idx
        return [
            fileid for doc_idx, fileid in enumerate(self.corpus.fileids())
            if doc_idx in indices
        ]

    def labels(self, fold=None, train=False, test=False):
        """
        Fit will load a list of the labels from the corpus categories.

        If a fold is specified (should be an integer between 0 and folds),
        then the loader will return documents from that fold. Further, train
        or test must be specified to split the fold correctly.
        """
        return [
            self.corpus.categories(fileids=fileid)[0]
            for fileid in self.fileids(fold, train, test)
        ]

    def documents(self, fold=None, train=False, test=False):
        """
        A generator of documents being streamed from disk. Each document is
        a list of paragraphs, which are a list of sentences, which in turn is
        a list of tuples of (token, tag) pairs. All preprocessing is done by
        NLTK and the CorpusReader object this object wraps.

        If a fold is specified (should be an integer between 0 and folds),
        then the loader will return documents from that fold. Further, train
        or test must be specified to split the fold correctly. This method
        allows us to maintain the generator properties of document reads.
        """
        for fileid in self.fileids(fold, train, test):
            yield list(self.corpus.tagged(fileids=fileid))


##########################################################################
## Normalize Transformer
##########################################################################

class TextNormalizer(BaseEstimator, TransformerMixin):
    """
    Takes a list of tokens, removes stopwords and punctuation and lowercases
    as well as lemmatizes the words for the first step in feature extraction.

    Note that this transformer expects as input to transform a list of tuples,
    (token, tag) pairs, that represent a single document.
    """

    def __init__(self, stopwords=None):
        self.stopwords  = set(stopwords or nltk.corpus.stopwords.words('english'))
        self.lemmatizer = nltk.WordNetLemmatizer()

    def is_punct(self, token):
        """
        Determines if the entire token is punctuation.
        """
        return all(
            unicodedata.category(char).startswith('P') for char in token
        )

    def is_stopword(self, token):
        """
        Determines if the token is a stopword or not.
        """
        return token.lower() in self.stopwords

    def tagwn(self, tag):
        """
        Returns the WordNet tag from the Penn Treebank tag.
        """
        return {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(tag[0], wn.NOUN)

    def lemmatize(self, token, tag):
        """
        Lemmatizes the token according to the part of speech tag.
        """
        return self.lemmatizer.lemmatize(token, self.tagwn(tag))

    def normalize(self, document):
        """
        Normalize each (token, tag) pair in the words data set.
        """
        return [
            self.lemmatize(token, tag).lower()
            for paragraph in document
            for sentence in paragraph
            for (token, tag) in sentence
            if not self.is_punct(token) and not self.is_stopword(token)
        ]

    def fit(self, X, y=None):
        """
        At the moment, fitting doesn't require any analysis.
        """
        return self

    def transform(self, documents):
        """
        Transform a corpus of documents into normalized features.
        """
        for document in documents:
            yield self.normalize(document)


##########################################################################
## Statitics Transformer
##########################################################################

class TextStats(BaseEstimator, TransformerMixin):
    """
    Computes the document statistics like length and number of sentences.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, documents):
        """
        Returns a dictionary of text features in advance of a DictVectorizer.
        """
        for document in documents:
            # Collect token and vocabulary counts
            counts = Counter(
                item[0] for para in document for sent in para for item in sent
            )

            # Yield structured information about the document
            yield {
                'paragraphs': len(document),
                'sentences': sum(len(para) for para in document),
                'words': sum(counts.values()),
                'vocab': len(counts),
            }


##########################################################################
## Model Building Functions
##########################################################################

def construct_pipeline(classifier):
    """
    This function creates a feature extraction pipeline that accepts data
    from a CorpusLoader and appends the classification model to the end of
    the pipeline, returning a newly constructed Pipeline object that is
    ready to be fit and trained!
    """

    return Pipeline([
        # Create a Feature Union of Text Stats and Bag of Words
        ('union', FeatureUnion(
            transformer_list = [

                # Pipeline for pulling document structure features
                ('stats', Pipeline([
                    ('stats', TextStats()),
                    ('vect', DictVectorizer()),
                ])),

                # Pipeline for creating a bag of words TF-IDF vector
                ('bow', Pipeline([
                    ('tokens', TextNormalizer()),
                    ('tfidf',  TfidfVectorizer(
                        tokenizer=identity, preprocessor=None, lowercase=False
                    )),
                    ('best', TruncatedSVD(n_components=1000)),
                ])),

            ],

            # weight components in feature union
            transformer_weights = {
                'stats': 0.15,
                'bow': 0.85,
            },
        )),

        # Append the estimator to the end of the pipeline
        ('classifier', classifier),
    ])


@timeit
def build_model(loader, model, **kwargs):
    """
    This function creates a pipeline from the feature extraction method in
    construct_pipeline and the passed in model and model keyword arguments,
    then trains the model with the given loader using all folds, then the
    complete dataset given by the loader object. It returns the fitted
    pipeline object along with scores and timing information.
    """

    # TODO: Add multiprocessing to parallelize build_inner_fold
    # TODO: Add verbosity to inform user on command line what is happening
    # TODO: Equip this method to be used by Celery workers

    @timeit
    def build_inner_fold(loader, classifier, fold=None):
        """
        A timed inner function that will return a set of evaluation scores
        if a fold is passed in, otherwise will build the model on the entire
        dataset and return the fitted model.
        """

        # Get the training data from the loader
        X_train = list(loader.documents(fold, train=True))
        y_train = list(loader.labels(fold, train=True))

        # Construct the pipeline from the instantiated classifier
        model = construct_pipeline(classifier)
        model.fit(X_train, y_train)

        # If folds is None, then return the fitted model.
        if fold is None: return model

        # Otherwise get the test data from the fold to perform an evaluation.
        X_test  = list(loader.documents(fold, test=True))
        y_test  = list(loader.labels(fold, test=True))
        y_pred  = model.predict(X_test)

        # Get the per-class scores as a well-structured object
        keys = ('precision', 'recall', 'f1', 'support')
        scores = precision_recall_fscore_support(y_test, y_pred, labels=model.classes_)
        scores = map(lambda s: dict(zip(model.classes_, s)), scores)
        scores = dict(zip(keys, scores))

        # Get the weighted scores and add to the scores object
        weighted = precision_recall_fscore_support(y_test, y_pred, average='weighted', pos_label=None)
        for key, wscore in zip(keys, weighted):
            scores[key]['average'] = float(wscore) if wscore is not None else None

        return scores


    # Now that the inner function works, let's run the model build process on
    # each fold for cross-validation and a final time to complete the model.
    scores = defaultdict(lambda: defaultdict(list))
    for fold in range(loader.n_folds):

        classifier  = model(**kwargs)                            # Instantiate the classifier
        score, time = build_inner_fold(loader, classifier, fold) # Fit the model for this fold

        # Update the scores as a list of scores for each run
        for name, values in score.items():
            for label, value in values.items():
                scores[name][label].append(value)

        # Add the time to the scores listing
        scores['times']['folds'].append(time)

    # Build the final model
    classifier = model(**kwargs)
    classifier, build_time = build_inner_fold(loader, classifier)
    scores['times']['final'] = build_time

    # Return everything we've constructed (*whew)
    return classifier, scores


if __name__ == '__main__':
    import os
    import pickle

    from corpus.reader import TranscriptCorpusReader
    from sklearn.linear_model import LogisticRegression

    path   = os.path.join(os.path.dirname(__file__), "fixtures", "debates")
    saveto = os.path.join(os.path.dirname(__file__), "fixtures", "maxent-debates.pickle")
    corpus = TranscriptCorpusReader(path)
    loader = CorpusLoader(corpus, 12)

    model  = LogisticRegression
    (model, scores), total_time = build_model(loader, model)

    with open(saveto, 'wb') as f:
        pickle.dump(model, f)

    with open('scores.pickle', 'wb') as f:
        pickle.dump(scores, f)

    print("Finished build process in {}".format(total_time))
