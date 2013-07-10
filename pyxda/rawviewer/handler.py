#!/usr/bin/env python

from enthought.traits.ui.api import Handler

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
