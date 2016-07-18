# corpus.signals
# Signals for model management in the corpus app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Jul 17 21:05:28 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals for model management in the corpus app.
"""

##########################################################################
## Imports
##########################################################################

import bs4
import requests

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from corpus.bitly import shorten
from corpus.models import Document
from partisan.utils import signature
from corpus.exceptions import FetchError
from corpus.nlp import preprocess, word_vocab_count


##########################################################################
## Document Signals
##########################################################################

@receiver(pre_save, sender=Document)
def fetch_document_on_create(sender, instance, *args, **kwargs):
    """
    This is the workhorse of the document saving model. If the document is
    created and doesn't have a short url, it will fetch a short url. If the
    document is created and doesn't have html, it will fetch the html.
    """

    # Fetch the bit.ly URL if it doesn't already have one.
    if not instance.short_url:
        instance.short_url = shorten(instance.long_url)

    # If there is no raw_html, fetch it with the requests module.
    if not instance.raw_html:

        try:
            # Get the response and check if it exists
            # Raise an exception on a bad status code
            response = requests.get(instance.long_url)
            response.raise_for_status()
        except Exception as e:
            raise FetchError(
                "Could not fetch document: {}".format(e)
            )

        # Otherwise set the raw html on the instance
        instance.raw_html = response.text

    # If there is no content, preprocess it
    if not instance.content:
        instance.content = preprocess(instance.raw_html)
        words, vocab = word_vocab_count(instance.content)
        instance.n_words = words
        instance.n_vocab = vocab

    # If there is no title, parse it from the raw html.
    if not instance.title:
        soup = bs4.BeautifulSoup(instance.raw_html, 'lxml')
        instance.title = soup.title.string

    # If there is no signature parse it from the raw_html
    # TODO: Change the signature to operate off the preprocessed text.
    if not instance.signature:
        instance.signature = signature(instance.raw_html)
