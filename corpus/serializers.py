# corpus.serializers
# API serializers for corpus models and API interaction.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 18 09:30:17 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
API serializers for corpus models and API interaction.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import serializers
from corpus.models import Document, Annotation
from django.core.validators import URLValidator

##########################################################################
## Document Serializer
##########################################################################

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Only allows the POST/PUT of a long_url and shows the document detail.
    """

    labels = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model  = Document
        fields = (
            'url', 'title', 'long_url', 'short_url',
            'signature', 'n_words', 'n_vocab', 'labels',
        )
        read_only_fields = (
            'title', 'short_url', 'signature', 'n_words', 'n_vocab',
        )
        extra_kwargs = {
            'long_url': {'validators': []},
            'url': {'view_name': 'api:document-detail'},
        }
