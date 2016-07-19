# corpus.views
# Views for the corpus application
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Jul 17 19:33:46 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the corpus application
"""

##########################################################################
## Imports
##########################################################################

from django.views.generic import DetailView

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from corpus.models import Document, Annotation, Label
from corpus.serializers import DocumentSerializer
from corpus.serializers import AnnotationSerializer
from corpus.exceptions import CorpusException


##########################################################################
## Views
##########################################################################

class DocumentDetail(DetailView):

    model = Document
    template_name = 'corpus/document.html'
    context_object_name = 'document'
    labels_parent_name  = 'USA Political Parties'


    def get_context_data(self, **kwargs):
        context = super(DocumentDetail, self).get_context_data(**kwargs)

        # Add user-specific parameters
        document   = context['document']
        annotation = document.annotations.filter(user=self.request.user).first()
        context['annotation'] = annotation

        # Add label-specific parameters
        # TODO Do not hard code the parent into the class!
        context['labels'] = Label.objects.filter(
            parent__name = self.labels_parent_name
        )

        return context

##########################################################################
## API HTTP/JSON Views
##########################################################################

class DocumentViewSet(viewsets.ModelViewSet):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create both the document and the annotation (user-association).
        """
        # Deserialize and validate the data from the user.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Execute the document and annotation creation
        self.perform_create(serializer)

        # Get the headers and return a response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Excepts any thing that might happen in the signals and raises a
        validation error in order to send back the right status code.
        """
        try:

            # Create the document object
            long_url = serializer.validated_data['long_url']
            document, _ = Document.objects.get_or_create(long_url=long_url)
            serializer.instance = document

            # Create the annotation object
            annotate, _ = Annotation.objects.get_or_create(
                user = self.request.user, document = document
            )

        except CorpusException as e:
            raise ValidationError(str(e))

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def annotate(self, request, pk=None):
        """
        Allows the specification of an annotation (label) for the given
        document. Note that a user can only have one label associated with
        one document, for the time being.
        """

        # Get the document of the detail view and deserialize data
        document   = self.get_object()
        serializer = AnnotationSerializer(
            data=request.data,
            context={'request': request, 'document': document}
        )

        # Validate the serializer and save the annotation
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return the response
        return Response(serializer.data)
