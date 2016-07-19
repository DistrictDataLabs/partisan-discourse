# corpus.admin
# Register models with the Django Admin for the corpus app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Jul 17 19:30:33 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [2de4867] benjamin@bengfort.com $

"""
Register models with the Django Admin for the corpus app.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from corpus.models import Document, Annotation, Label

##########################################################################
## Register Admin
##########################################################################

admin.site.register(Label)
admin.site.register(Annotation)
admin.site.register(Document)
