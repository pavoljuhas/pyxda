#!/usr/bin/env python
# coding=utf-8
##############################################################################
#
# pyxda.srxes       X-ray Data Analysis Library
#                   (c) 2013 National Synchrotron Light Source II,
#                   Brookhaven National Laboratory, Upton, NY.
#                   All rights reserved.
#
# File coded by:    <FileAuthor>
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

"""Test if pyxda can be imported and if the testdata directory is available.
"""

import os
import unittest

from pyxda.tests.testutils import datafile

##############################################################################
class TestBareBones(unittest.TestCase):

    def setUp(self):
        return


    def tearDown(self):
        return


    def test_testdata_dir(self):
        """check if the testdata directory exists.
        """
        self.assertTrue(os.path.isdir(datafile('')))
        self.assertTrue(os.path.isfile(datafile('empty.txt')))
        return

# End of class TestAttributes

if __name__ == '__main__':
    unittest.main()
