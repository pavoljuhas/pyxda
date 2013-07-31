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

"""Subpackage for unit tests.  Unit tests kickstart functions.
"""

def testsuite():
    '''Build a unit tests suite for the pyxda package.

    Return a unittest.TestSuite object.
    '''
    import unittest
    modulenames = '''
        pyxda.tests.testbarebones
    '''.split()
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for mname in modulenames:
        exec ('import %s as mobj' % mname)
        suite.addTests(loader.loadTestsFromModule(mobj))
    return suite


def test():
    '''Execute all unit tests for the diffpy.srreal package.
    Return a unittest TestResult object.
    '''
    import unittest
    suite = testsuite()
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result
