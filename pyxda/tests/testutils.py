#!/usr/bin/env python
# coding=utf-8
##############################################################################
#
# pyxda             X-ray Data Analysis Library
#
# File coded by:    FIXME
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
