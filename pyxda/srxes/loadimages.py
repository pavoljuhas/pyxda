#!/usr/bin/env python
# coding=utf-8
##############################################################################
#
# pyxda.srxes       X-ray Data Analysis Library
#                   (c) 2013 National Synchrotron Light Source II,
#                   Brookhaven National Laboratory, Upton, NY.
#                   All rights reserved.
#
# File coded by:    Michael Saltzman
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

import os
from traits.api import HasTraits
import threading
import glob

# TODO: Enable Live Mode
class LoadImage(HasTraits, threading.Thread):
    '''A separate thread that searches the given directory for .tif images.
    For each image, it sends a request to the ProcessCenter to store the
    image. A thread is created and run each time a directory is chosen.

    NOTE: Images are not loaded into memory but their paths are stored so 
    loading can be performed at a later time.
    '''
    def __init__(self, queue, dirpath):
        threading.Thread.__init__(self)
        super(LoadImage, self).__init__() 

        self.dirpath = dirpath
        self.filelist = []

        self.jobqueue = queue
        self.backgroundenable = False
        self.daemon = True

    def run(self):
        print 'Live mode start'
        self.initLive()
        self.livemode()
        print 'Live mode stop'
        return

    def initLive(self):
        '''Creates a list of valid .tif files in the directory.'''
        if os.path.isdir(self.dirpath):
            self.filelist = glob.glob(self.dirpath + '/*.tif')
            if not self.filelist:
                msg = 'WARNING: No .tif images found.'
                print msg
            else:
                msg = ''
        else:
            msg = 'WARNING: Not a valid directory.'
            print msg
        self.jobqueue.put(['updatemsg', msg])
        return

    def livemode(self):
        '''Sends image requests to the ProcessCenter for each image.'''
        for i in range(len(self.filelist)):
            self.jobqueue.put(['newimage', {'path':self.filelist[i]}])
            print self.filelist[i]
            #print 'Image Process Sent'
            if i == 2:
                self.jobqueue.put(['initcache'])
        return

if __name__ == '__main__':
    '''
    dirpath = '/Users/Mike/Downloads/1208NSLSX17A_LiRh2O4/'
    output = getTiffImages(dirpath)
    print output
    '''
