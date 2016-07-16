# partisan.settings.production
# The Django settings for partisan-discourse in production
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Jul 16 11:29:09 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: production.py [] benjamin@bengfort.com $

"""
The Django settings for partisan-discourse in production
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Production Settings
##########################################################################

## Debugging Settings
DEBUG            = False

## Hosts
ALLOWED_HOSTS    = [
    'partisan-discourse.herokuapp.com',
    'partisan.districtdatalabs.com',
    'partisan-discourse.districtdatalabs.com',
]

## Static files served by WhiteNoise
STATIC_ROOT = os.path.join(PROJECT, 'staticfiles')
