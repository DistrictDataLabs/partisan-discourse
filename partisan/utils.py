# partisan.utils
# Project level  utilities and helpers
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 22:26:18 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: utils.py [] benjamin@bengfort.com $

"""
Project level  utilities and helpers
"""

##########################################################################
## Imports
##########################################################################

import re
import base64
import bleach
import hashlib
import requests

from functools import wraps
from markdown import markdown
from django.conf import settings
from urllib.parse import urljoin


##########################################################################
## Utilities
##########################################################################

## Nullable kwargs for models
nullable = { 'blank': True, 'null': True, 'default':None }

## Not nullable kwargs for models
notnullable = { 'blank': False, 'null': False }

##########################################################################
## Helper functions
##########################################################################


def normalize(text):
    """
    Normalizes the text by removing all punctuation and spaces as well as
    making the string completely lowercase.
    """
    return re.sub(r'[^a-z0-9]+', '', text.lower())


def signature(text):
    """
    This helper method normalizes text and takes the SHA1 hash of it,
    returning the base64 encoded result. The normalization method includes
    the removal of punctuation and white space as well as making the case
    completely lowercase. These signatures will help us discover textual
    similarities between questions.
    """
    return base64.b64encode(hashlib.sha256e(normalize(text)).digest())


def htmlize(text):
    """
    This helper method renders Markdown then uses Bleach to sanitize it as
    well as convert all links to actual links.
    """
    text = bleach.clean(text, strip=True)    # Clean the text by stripping bad HTML tags
    text = markdown(text)                    # Convert the markdown to HTML
    text = bleach.linkify(text)              # Add links from the text and add nofollow to existing links

    return text


def bitly_shorten(url, token=None):
    """
    Shortens a URL using the bit.ly API.
    """

    # Get the bit.ly access token from settings
    token = settings.BITLY_ACCESS_TOKEN or token
    if not token:
        raise ValueError(
            "Cannot call shorten URL without a bit.ly access token"
        )

    # Compute and make the request to the API
    endpoint = urljoin(settings.BITLY_API_ADDRESS, "v3/shorten")
    params = {
        "access_token": token,
        "longUrl": url,
    }

    # bit.ly tends not to send status code errors
    response = requests.get(endpoint, params=params)

    # Parse and return the result
    data = response.json()
    if data['status_code'] != 200:
        raise ValueError(data['status_txt'])
    return data['data']['url']


##########################################################################
## Memoization
##########################################################################


def memoized(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent
    accesses is returned, preventing the need to call the getter any more.
    https://github.com/estebistec/python-memoized-property
    """
    attr_name = '_{0}'.format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)
