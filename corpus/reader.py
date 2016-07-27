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

from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader


##########################################################################
## Module Constants
##########################################################################

DOC_PATTERN = r'(?!\.)[\w_\s]+/[\w\s\d\-]+\.txt'
CAT_PATTERN = r'([\w_\s]+)/.*'


##########################################################################
## Corpus Reader
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
