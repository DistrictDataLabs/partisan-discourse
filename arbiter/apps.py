# arbiter.apps
# Application definition for the arbiter app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Aug 02 09:14:47 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [] benjamin@bengfort.com $

"""
Application definition for the arbiter app.
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig


##########################################################################
## Corpus Config
##########################################################################

class ArbiterConfig(AppConfig):

    name = 'arbiter'
    verbose_name = 'Arbiter'

    def ready(self):
        pass
        # import arbiter.signals
