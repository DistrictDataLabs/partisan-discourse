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
from django.apps import apps

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


##########################################################################
## Corpus Manager
##########################################################################

class CorpusManager(models.Manager):

    def create_for_user(self, user, **kwargs):
        """
        Creates a user-specific corpus containing all the documents that the
        user has tagged to date. Can pass in any additional fields as well.
        """
        # Lazy load the document model
        Document = apps.get_model('corpus.Document')
        LabeledDocument = apps.get_model('corpus.LabeledDocument')

        # Add the user to the kwargs and construct the corpus.
        kwargs['user'] = user
        corpus = self.create(**kwargs)

        # Now add all the documents the user has annotated to date.
        for doc in Document.objects.filter(annotations__user=user):
            if corpus.labeled:
                label = doc.label(user)
                if label is None: continue
            else:
                label = None

            LabeledDocument.objects.create(
                corpus=corpus, document=doc, label=label,
            )

        return corpus
