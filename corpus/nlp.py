# corpus.nlp
# Provides utilities for natural language processing
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 18 11:55:41 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: nlp.py [f8db174] benjamin@bengfort.com $

"""
Provides utilities for natural language processing
"""

##########################################################################
## Imports
##########################################################################

import bs4
import nltk

from collections import Counter
from readability.readability import Document

##########################################################################
## Module Constants
##########################################################################

# Tags to extract as paragraphs from the HTML text
TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li'
]


##########################################################################
## Preprocessing Functions
##########################################################################

def para_tokenize(html):
    """
    Splits an HTML document into consistutent paragraphs.
    """
    # Transform the document into a readability paper summary
    summary = Document(html).summary()

    # Parse the HTML using BeautifulSoup
    soup = bs4.BeautifulSoup(summary, 'lxml')

    # Extract the paragraph delimiting elements
    for tag in soup.find_all(TAGS):

        # Get the HTML node text
        text = tag.get_text()
        if text: yield text


def preprocess(html):
    """
    Returns a preprocessed document consisting of a list of paragraphs, which
    is a list of sentences, which is a list of tuples, where each tuple is a
    (token, part of speech) pair.
    """
    return [
        [
            nltk.pos_tag(nltk.wordpunct_tokenize(sent))
            for sent in nltk.sent_tokenize(paragraph)
        ]
        for paragraph in para_tokenize(html)
    ]


def word_vocab_count(text):
    """
    Counts the number of words and vocabulary in preprocessed text.
    """
    counts = Counter([
        word[0].lower()
        for paragraph in text
        for sentence in paragraph
        for word in sentence
    ])

    return sum(counts.values()), len(counts)
