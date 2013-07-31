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

from traitsui.api import Handler

class PyXDAHandler(Handler):
    def close(self, info, is_OK):
        '''
        if ( info.object.panel.acquisition_thread
            and info.object.panel.acquisition_thread.isAlive() ):
            info.object.panel.acquisition_thread.wants_abort = True
            while info.object.panel.acquisition_thread.isAlive():
                sleep(0.1)
           wx.Yield()
        '''   
        return True
