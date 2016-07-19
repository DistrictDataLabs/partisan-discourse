# corpus.managers
# Model managers for the corpus application.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 18 23:09:19 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: managers.py [bab00b2] benjamin@bengfort.com $

"""
Model managers for the corpus application.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models


##########################################################################
## Annotation Manager
##########################################################################

class AnnotationManager(models.Manager):

    def republican(self):
        """
        Filters the annotations for only republican annotations.
        """
        return self.filter(label__slug='republican')

    def democratic(self):
        """
        Filters the annotations for only democratic annotations.
        """
        return self.filter(label__slug='democratic')
