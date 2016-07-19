# corpus.apps
# Application definition for the corpus app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Jul 17 19:31:28 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [2de4867] benjamin@bengfort.com $

"""
Application definition for the corpus app.
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig


##########################################################################
## Corpus Config
##########################################################################

class CorpusConfig(AppConfig):

    name = 'corpus'
    verbose_name = "Corpora"

    def ready(self):
        import corpus.signals
