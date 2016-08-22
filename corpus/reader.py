# corpus.reader
# A simple corpus reader object for training models.
#
# Author:   Tony Ojeda <tojeda@districtdatalabs.com>
# Created:  Mon Jul 25 17:14:45 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: reader.py [] tojeda@districtdatalabs.com $

"""
A simple corpus reader object for training models.
"""

##########################################################################
## Imports
##########################################################################

import os
import nltk

from corpus.models import Label
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader


##########################################################################
## Module Constants
##########################################################################

DOC_PATTERN = r'(?!\.)[\w_\s]+/[\w\s\d\-]+\.txt'
CAT_PATTERN = r'([\w_\s]+)/.*'


##########################################################################
## Transcript Corpus Reader
##########################################################################

class TranscriptCorpusReader(CategorizedPlaintextCorpusReader):

    def __init__(self, root, **kwargs):
        CategorizedPlaintextCorpusReader.__init__(
        	self, root, DOC_PATTERN, cat_pattern=CAT_PATTERN
        )

    def tagged(self, **kwargs):
        """
        Returns part-of-speech tagged words in sentences in paragraphs.
        """
        for para in self.paras(**kwargs):
            yield [
                nltk.pos_tag(sent) for sent in para
            ]


##########################################################################
## Django Query Corpus Reader
##########################################################################

class QueryCorpusReader(object):
    """
    The query corpus reader takes in a query that yields a list of documents
    and modifies it such that it is only fetching the preprocessed content in
    a streaming fashion.
    """

    def __init__(self, query, user=None):
        """
        Pass in a QuerySet or Query object for selecting a group of documents.
        Can also optionally pass in a user to determine labeling scheme.
        """
        self.user  = user
        self.query = query

    def fileids(self, categories=None):
        """
        Returns a list of file primary keys for the files that make up this
        corpus or that make up the given category(s) if specified.

        Categories can be either a single string or a list of strings.
        """
        # If categories is None, return all fileids.
        if categories is None:
            return self.query.values_list('id', flat=True)

        # Convert to a list if a singleton is passed
        if isinstance(categories, (str, Label)):
            categories = [categories,]

        # Convert to a quick lookup data structure
        categories = set(categories)

        # Manually loop through all documents (bummer)
        return [
            doc.id for doc in self.query
            if doc.label(self.user) in categories
        ]

    def categories(self, fileids=None):
        """
        Return a list of file identifiers of the categories defined for this
        corpus or the file(s) if it is given.

        Fileids can be either a list of integers or a single integer.
        """
        # If fileids is None, return all categories
        # HACK: use a unique query on the database
        if fileids is None:
            return list(set([
                str(doc.label(self.user)) for doc in self.query
            ]))

        # Convert to a list if a singleton is passed
        if isinstance(fileids, int):
            fileids = [fileids,]

        return list(set([
            str(doc.label(self.user))
            for doc in self.query.filter(id__in=fileids)
        ]))

    def tagged(self, fileids=None, categories=None):
        """
        Returns the content of each document.
        """
        if fileids is None:
            fileids = self.fileids(categories)

        if isinstance(fileids, int):
            fileids = [fileids,]

        for doc in self.query.filter(id__in=fileids).values_list('content', flat=True):
            for para in doc:
                yield para


##########################################################################
## Django Corpus Model Reader
##########################################################################

class CorpusModelReader(QueryCorpusReader):
    """
    Takes a corpus object and automatically references documents.

    Note this class takes advantage of the LabeledDocument through model
    between documents and corpora in order to perform queries on the database.
    The QueryCorpusReader relies on the label() method of a document for
    label discovery and therefore cannot do filtering or querying based on
    data that is stored in the database.
    """

    def __init__(self, corpus):
        self.corpus = corpus
        super(CorpusModelReader, self).__init__(
            corpus.documents.all(), corpus.user
        )

    def fileids(self, categories=None):
        """
        Returns a list of file primary keys for the files that make up this
        corpus or that make up the given category(s) if specified.

        Categories can be either a single string or a list of strings.
        """
        # If categories is None, return all fileids.
        if categories is None:
            return self.query.values_list('id', flat=True)

        # Convert to a list if a singleton is passed
        if isinstance(categories, (str, Label)):
            categories = [categories,]

        # Convert to a quick lookup data structure
        categories = set(categories)

        # Filter the labeled documents based on the label.
        query = self.corpus.labels.filter(label__in=categories)
        return query.values_list('document_id', flat=True)

    def categories(self, fileids=None):
        """
        Return a list of file identifiers of the categories defined for this
        corpus or the file(s) if it is given.

        Fileids can be either a list of integers or a single integer.
        """
        # If fileids is None, return all categories
        if fileids is None:
            labels = self.corpus.labels.values_list('label', flat=True).distinct()
            return Label.objects.filter(id__in=labels).values_list('slug', flat=True)

        # Convert to a list if a singleton is passed
        if isinstance(fileids, int):
            fileids = [fileids,]

        labels = self.corpus.labels.filter(document_id__in=fileids)
        labels = labels.values_list('label', flat=True).distinct()
        return Label.objects.filter(id__in=labels).values_list('slug', flat=True)


if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), "fixtures", "debates")
    corpus = TranscriptCorpusReader(path)

    print("{} documents, {} categories".format(
        len(corpus.fileids()), len(corpus.categories())
    ))

    print(", ".join([
        "{} {} documents".format(len(corpus.fileids(categories=cat)), cat)
        for cat in corpus.categories()
    ]))

    print("{} paragraphs, {} sentences, {} words".format(
        len(corpus.paras()), len(corpus.sents()), len(corpus.words())
    ))
