# corpus.exceptions
# Custom exceptions for corpus handling.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 18 09:57:26 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: exceptions.py [63935bc] benjamin@bengfort.com $

"""
Custom exceptions for corpus handling.
"""

##########################################################################
## Corpus Exceptions
##########################################################################

class CorpusException(Exception):
    """
    Something went wrong in the corpus app.
    """
    pass


class BitlyAPIError(CorpusException):
    """
    Something went wrong trying to shorten a url.
    """
    pass


class FetchError(CorpusException):
    """
    Something went wrong trying to fetch a url using requests.
    """
    pass


class NLTKError(CorpusException):
    """
    Something went wrong when using NLTK.
    """
    pass
