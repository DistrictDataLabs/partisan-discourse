# corpus.models
# Database models for the corpus app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Jul 17 19:32:41 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [2de4867] benjamin@bengfort.com $

"""
Database models for the corpus app
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from autoslug import AutoSlugField
from partisan.utils import nullable
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from picklefield.fields import PickledObjectField
from corpus.managers import AnnotationManager, CorpusManager

##########################################################################
## Document Model
##########################################################################

class Document(TimeStampedModel):
    """
    Describes a document that is part of one or more corpora.
    """

    title     = models.CharField(max_length=255, **nullable)                 # The title of the document, extracted from HTML
    long_url  = models.URLField(max_length=2000, unique=True)                # The long url for the document
    short_url = models.URLField(max_length=30, **nullable)                   # The bit.ly shortened url
    raw_html  = models.TextField(**nullable)                                 # The html content fetched (hopefully)
    content   = PickledObjectField(**nullable)                               # The preprocessed NLP content in a parsable text representation
    signature = models.CharField(max_length=44, editable=False, **nullable)  # A base64 encoded hash of the content
    n_words   = models.SmallIntegerField(**nullable)                         # The word count of the document
    n_vocab   = models.SmallIntegerField(**nullable)                         # The size of the vocabulary used

    # Users are associated with documents by downloading and annotating them.
    users     = models.ManyToManyField(
        'auth.User', through='corpus.Annotation', related_name='documents'
    )

    class Meta:
        db_table = "documents"
        get_latest_by = "created"
        unique_together = ("long_url", "short_url")

    def get_absolute_url(self):
        """
        Returns the detail view url for the object
        """
        return reverse('corpus:document-detail', args=(self.id,))

    def __str__(self):
        if self.title: return self.title
        return self.short_url


##########################################################################
## Annotation
##########################################################################

class Label(TimeStampedModel):
    """
    A label that is associated with a document to classify it.
    """

    name      = models.CharField(max_length=64, unique=True)        # The name of the label
    slug      = AutoSlugField(populate_from='name', unique=True)    # A unique slug of the label
    parent    = models.ForeignKey('self', **nullable)               # If there is a label hierarchy
    documents = models.ManyToManyField(
        'corpus.Document', through='corpus.Annotation', related_name='labels'
    )

    class Meta:
        db_table = "labels"
        get_latest_by = "created"

    def __str__(self):
        return self.name


class Annotation(TimeStampedModel):
    """
    A user description of a document, e.g. what label and a user-specific
    association with the documentation for personalized corpus generation.
    """

    document  = models.ForeignKey('corpus.Document', related_name='annotations')
    user      = models.ForeignKey('auth.User', related_name='annotations')
    label     = models.ForeignKey('corpus.Label', related_name='annotations', **nullable)

    objects   = AnnotationManager()

    class Meta:
        db_table = "annotations"
        get_latest_by = "modified"
        ordering = ['-modified']
        unique_together = ("document", "user")

    def __str__(self):
        if self.label:
            return "{} added label {} to \"{}\" on {}".format(
                self.user, self.label, self.document, self.modified
            )

        return "{} added document \"{}\" on {}".format(
            self.user, self.document, self.created
        )


##########################################################################
## Corpus Model
##########################################################################

class Corpus(TimeStampedModel):
    """
    A model that maintains a mapping of documents to estimators for use in
    tracking the training data that is used to fit a text classifier object.
    """

    title     = models.CharField(max_length=255, **nullable)
    slug      = AutoSlugField(populate_from='title', unique=True)
    documents = models.ManyToManyField('corpus.Document', related_name='corpora')
    user      = models.ForeignKey('auth.User', related_name='corpora', **nullable)

    objects   = CorpusManager()

    class Meta:
        db_table = "corpora"
        get_latest_by = "created"
        ordering = ["-created"]
        verbose_name = "corpus"
        verbose_name_plural = "corpora"

    def __str__(self):
        if self.title:
            return self.title

        # Construct the descriptive string.
        s = "{} document corpus created on {}".format(
            self.documents.count(), self.created.strftime("%Y-%m-%d")
        )

        if self.user:
            s += " by {}".format(self.user)

        return s
