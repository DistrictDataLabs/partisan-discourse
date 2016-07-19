# partisan.tests.test_init
# Initialization tests for the Partisan Discourse project
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Jul 16 11:36:36 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: test_init.py [80822db] benjamin@bengfort.com $

"""
Initialization tests for the Partisan Discourse project
"""

##########################################################################
## Imports
##########################################################################

from unittest import TestCase

##########################################################################
## Module variables
##########################################################################

EXPECTED_VERSION = "0.1b2"

##########################################################################
## Initialization Tests
##########################################################################

class InitializationTests(TestCase):
    """
    Some basic partisan tests
    """

    def test_sanity(self):
        """
        Check that the world is sane and 2+2=4
        """
        self.assertEqual(2+2, 4)

    def test_import(self):
        """
        Ensure the partisan module can be imported
        """
        try:
            import partisan
        except ImportError:
            self.fail("Could not import the partisan module.")

    def test_version(self):
        """
        Assert that test and package versions match
        """
        import partisan
        self.assertEqual(EXPECTED_VERSION, partisan.__version__)
