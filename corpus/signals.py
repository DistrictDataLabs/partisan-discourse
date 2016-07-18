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

from corpus.models import Document
from partisan.utils import signature, bitly_shorten


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
        instance.short_url = bitly_shorten(instance.long_url)

    # If there is no raw_html, fetch it with the requests module.
    if not instance.raw_html:
        response = requests.get(instance.long_url)
        if response.status_code == 200:
            instance.raw_html = response.text
