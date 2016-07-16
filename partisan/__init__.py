# partisan
# The project module for the Partisan Discourse web application.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Jul 16 11:38:44 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
The project module for the Partisan Discourse web application.
"""

##########################################################################
## Imports
##########################################################################

from .version import get_version

##########################################################################
## Project Info
##########################################################################

__version__ = get_version()
