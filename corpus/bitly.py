# corpus.bitly
# Access the bit.ly url shortening service.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 18 09:59:27 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: bitly.py [] benjamin@bengfort.com $

"""
Access the bit.ly url shortening service.
"""

##########################################################################
## Imports
##########################################################################

import requests

from django.conf import settings
from urllib.parse import urljoin
from corpus.exceptions import BitlyAPIError

##########################################################################
## Shorten function
##########################################################################

def shorten(url, token=None):
    """
    Shortens a URL using the bit.ly API.
    """

    # Get the bit.ly access token from settings
    token = settings.BITLY_ACCESS_TOKEN or token
    if not token:
        raise BitlyAPIError(
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
        raise BitlyAPIError(
            "Could not shorten link: {}".format(data['status_txt'])
        )
    return data['data']['url']
