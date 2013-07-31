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

"""Convenience module for executing all unit tests with

python -m pyxda.tests.run
"""


if __name__ == '__main__':
    import sys
    from pyxda.tests import test
    # produce zero exit code for a successful test
    sys.exit(not test().wasSuccessful())

# End of file
