# corpus.urls
# URLs for routing the corpus app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 18 13:10:24 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: urls.py [f8db174] benjamin@bengfort.com $

"""
URLs for routing the corpus app.
"""

##########################################################################
## Imports
##########################################################################

from django.conf.urls import url
from corpus.views import *

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = (
    url(r'^documents/(?P<pk>\d+)/$', DocumentDetail.as_view(), name='document-detail'),
)
