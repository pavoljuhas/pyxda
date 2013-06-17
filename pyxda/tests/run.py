#!/usr/bin/env python
# coding=utf-8
##############################################################################
#
# pyxda             X-ray Data Analysis Library
#
# File coded by:    Pavol Juhas
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
