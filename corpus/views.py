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

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from corpus.models import Document, Annotation
from corpus.serializers import DocumentSerializer
from corpus.exceptions import CorpusException


##########################################################################
## Views
##########################################################################


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
