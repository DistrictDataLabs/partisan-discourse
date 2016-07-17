# partisan.wsgi
# WSGI Config for the Partisan Discourse project
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Jul 16 11:23:21 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: wsgi.py [5277a6e] benjamin@bengfort.com $

"""
WSGI config for partisan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

##########################################################################
## Imports
##########################################################################

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


##########################################################################
## Configuration
##########################################################################

## Load settings from environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partisan.settings.production")

## Create Whitenoise application
application = get_wsgi_application()
application = DjangoWhiteNoise(application)
