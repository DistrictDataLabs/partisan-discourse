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

import requests

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from corpus.bitly import shorten
from corpus.models import Document
from partisan.utils import signature
from corpus.exceptions import FetchError

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
