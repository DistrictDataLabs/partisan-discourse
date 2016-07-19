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
from corpus.models import Document, Annotation, Label


##########################################################################
## Document Serializer
##########################################################################

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Only allows the POST/PUT of a long_url and shows the document detail.
    """

    detail = serializers.URLField(source='get_absolute_url', read_only=True)
    labels = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model  = Document
        fields = (
            'url', 'detail', 'title', 'long_url', 'short_url',
            'signature', 'n_words', 'n_vocab', 'labels',
        )
        read_only_fields = (
            'title', 'short_url', 'signature', 'n_words', 'n_vocab',
        )
        extra_kwargs = {
            'long_url': {'validators': []},
            'url': {'view_name': 'api:document-detail'},
        }


##########################################################################
## Annotation/Label Serializer
##########################################################################

class CurrentDocumentDefault(object):

    def set_context(self, serializer_field):
        self.document = serializer_field.context['document']

    def __call__(self):
        return self.document

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)


class AnnotationSerializer(serializers.ModelSerializer):

    # The user that is doing the annotation
    user     = serializers.HyperlinkedRelatedField(
        default    = serializers.CurrentUserDefault(),
        read_only  = True,
        view_name  = "api:user-detail",
    )

    # The document that the user is annotating
    # Read only is true because the document is passed in at save.
    document = serializers.HyperlinkedRelatedField(
        view_name  = "api:document-detail",
        read_only  = True,
        default    = CurrentDocumentDefault(),
    )

    # The label the user is assigning to the document
    label    = serializers.SlugRelatedField(
        many       = False,
        slug_field = 'slug',
        queryset   = Label.objects.all(),
        allow_null = True,
     )

    class Meta:
        model  = Annotation
        fields = ('user', 'document', 'label')

    def create(self, validated_data):
        """
        Most annotations have already been created (so usually only update is
        needed), yet this serializer will not be instantiated with anything
        but document/user pairs - so we should look up the instance on save.
        """
        ModelClass = self.Meta.model

        try:
            self.instance = ModelClass.objects.get(
                user=validated_data['user'],
                document=validated_data['document'],
            )
            return self.update(self.instance, validated_data)
        except ModelClass.DoesNotExist:
            return super(AnnotationSerializer, self).create(validated_data)
