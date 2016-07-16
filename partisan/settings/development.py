# partisan.settings.development
# The Django settings for partisan-discourse in development.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Jul 16 11:29:36 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: development.py [] benjamin@bengfort.com $

"""
The Django settings for partisan-discourse in development.
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Development Settings
##########################################################################

## Debugging Settings
DEBUG            = True

## Hosts
ALLOWED_HOSTS    = ('127.0.0.1', 'localhost')

## Content
MEDIA_ROOT       = os.path.join(PROJECT, 'media')
STATIC_ROOT      = 'staticfiles'
