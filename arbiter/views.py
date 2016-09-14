# arbiter.views
# Views for the arbiter app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Aug 02 09:17:46 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the arbiter app.
"""

##########################################################################
## Imports
##########################################################################


from django.shortcuts import render
from arbiter.models import Estimator
from arbiter.serializers import EstimatorSerializer, PredictionSerializer
from corpus.models import Document
from corpus.reader import QueryCorpusReader
from corpus.learn import CorpusLoader

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

##########################################################################
## API HTTP/JSON Views
##########################################################################

class EstimatorViewSet(viewsets.ModelViewSet):

    queryset = Estimator.objects.all()
    serializer_class = EstimatorSerializer
    permission_classes = [IsAuthenticated]

    @detail_route(methods=['post'])
    def predict(self, request, pk=None, *args, **kwargs):
        # predict with a given Estimator against either a document ID or long url
        # get the Estimator
        if not pk:
            raise Exception("You must specify an Estimator")
        estimator_object = Estimator.objects.get(pk=pk)
        estimator_model = estimator_object.estimator

        # get the document
        if request.data.get("document_pk"):
            reader = QueryCorpusReader(Document.objects.filter(pk=request.data.get("document_pk")))
        elif request.data.get("document_long_url"):
            document = Document.objects.get_or_create(long_url=request.data.get("document_long_url"))[0]
            reader = QueryCorpusReader(Document.objects.filter(pk=document.pk))
        else:
            raise Exception("You must specify a Document!")

        # predict
        loader = CorpusLoader(reader)
        X = list(loader.documents())
        prediction = estimator_model.predict(X)

        # serialize prediction data
        serializer = PredictionSerializer({"prediction":prediction[0]})

        return Response(serializer.data)