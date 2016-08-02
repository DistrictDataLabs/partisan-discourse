# arbiter.admin
# Django admin CMS definitions and registrations for the arbiter app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Aug 02 09:18:18 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Django admin CMS definitions and registrations for the arbiter app.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from arbiter.models import Estimator, Score

##########################################################################
## Register Admin
##########################################################################

admin.site.register(Estimator)
admin.site.register(Score)
