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

"""Helper routines for running other unit tests.
"""

def datafile(filename):
    import os.path
    mydir = os.path.dirname(__file__)
    rv = os.path.join(mydir, 'testdata', filename)
    return rv
