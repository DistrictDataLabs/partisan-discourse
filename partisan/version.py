# partisan.version
# Helper module for managing versioning information
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Jul 16 11:37:27 2016 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: version.py [80822db] benjamin@bengfort.com $

"""
Helper module for managing versioning information
"""

##########################################################################
## Versioning
##########################################################################

__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 0,
    'releaselevel': 'beta',
    'serial': 3,
}


def get_version(short=False):
    """
    Returns the version from the version info.
    """
    if __version_info__['releaselevel'] not in ('alpha', 'beta', 'final'):
        raise ValueError(
            "unknown release level '{}', select alpha, beta, or final.".format(
                __version_info__['releaselevel']
            )
        )

    vers = ["{major}.{minor}".format(**__version_info__)]

    if __version_info__['micro']:
        vers.append(".{micro}".format(**__version_info__))

    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('{}{}'.format(__version_info__['releaselevel'][0],
                                  __version_info__['serial']))

    return ''.join(vers)
