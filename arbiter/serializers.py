# arbiter.serializers
# API serializers for arbiter models and API interaction.
#
# Author:   Laura Lorenz <llorenz@districtdatalabs.com>
# Created:  Tue Aug 23 19:48:23 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: serializers.py [] lalorenz6@gmail.com $

"""
API serializers for arbiter models and API interaction.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import serializers
from arbiter.models import Score, Estimator
from django.contrib.auth.models import User


##########################################################################
## Scores Serializer
##########################################################################

class ScoresSerializer(serializers.ModelSerializer):
    """
    Allows GET/DELETE of an id to retrieve/delete a Score.
    """

    class Meta:
        model = Score
        fields = (
            'metric',  'score', 'label', 'folds', 'estimator',
        )


##########################################################################
## Estimator Serializer
##########################################################################

class EstimatorSerializer(serializers.ModelSerializer):
    """
    Allows GET/POST/PUT/DELETE of an id to retrieve/predict/update/delete
    an Estimator.
    """
    #TODO: hyperlinked instead of nested for scores?
    scores = ScoresSerializer(many=True, read_only=True)

    # The user that generated the model
    owner = serializers.HyperlinkedRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        view_name="api:user-detail",
    )

    class Meta:
        model  = Estimator

        # TODO: will we ever need a serialization of the Estimator.estimator Pipeline pickle?
        exclude = (
            'estimator',
        )


class PredictionSerializer(serializers.Serializer):
    prediction = serializers.CharField(max_length=200)

    #TODO: do we care about more metadata about a given prediction? should we save these for cache?
