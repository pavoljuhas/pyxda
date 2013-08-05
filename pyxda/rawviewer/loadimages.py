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
import numpy as np
import re
import time
from enthought.traits.api import Dict, Instance, Directory, HasTraits
import threading
import glob

# TODO: Enable Live Mode
class LoadImage(HasTraits, threading.Thread):

    def __init__(self, queue, dirpath):
        threading.Thread.__init__(self)
        super(LoadImage, self).__init__() 

        self.dirpath = dirpath
        self.filelist = []

        self.jobqueue = queue
        self.backgroundenable = False
        self.daemon=True

    def run(self):
        print 'Live mode start'
        self.initLive()
        self.livemode()
        print 'Live mode stop'
        return

    def initLive(self):
        while True:
            if self.dirpath == '':
                time.sleep(0.5)
            elif os.path.isdir(self.dirpath):
                self.filelist = glob.glob(self.dirpath + '/*.tif')
                break
                '''dirlist = os.listdir(self.dirpath)
                for f in dirlist:
                    if f[-4:] == "tiff" or f[-3:] == "tif":
                        self.filelist.append(f)
                break
            else:
                print 'No data found or directory does not exist. (LoadImage)'
                '''
        '''
        self.startime = time.time()
        self.lastmtime = os.path.getmtime(self.dirpath)
        self.lastctime = os.path.getctime(self.dirpath)
        self.lastatime = os.path.getatime(self.dirpath)
        '''
        return

    def livemode(self):
        #TODO: Hard Coded
        '''
        while True:
            
            if self.checkTime(self.tifdirectory):di
                newexistfileset = self.genFileSet() 
                newfileset = newexistfileset - self.existfileset
                newfilelist = sorted(list(newfileset))
                newfilelistfull = map(lambda name: os.path.abspath(self.tifdirectory+'/'+name), newfilelist)
                if len(newfilelist)>0:
                    for newfile in newfilelistfull:
                        self.checkFileVal(newfile)

            #self.existfileset = newexistfileset
            #    else:
            #        time.sleep(0.5)
            #else:
            #    time.sleep(0.5)

        '''
        for i in range(len(self.filelist)):
            self.jobqueue.put(['newimage', {'path':self.filelist[i]}])
            print self.filelist[i]
            #print 'Image Process Sent'
            if i == 2:
                self.jobqueue.put(['initcache'])
        return

    def checkTime(self, tifpath):
        if tifpath != self.lasttifdirectory:
            self.initLive()
            flag = False
        else:
            flag = False
            if os.path.getatime(tifpath) != self.lastatime:
                flag = True
                self.lastatime = os.path.getatime(tifpath)
                #print 'atime'+str(self.lastatime)
            if os.path.getmtime(tifpath) != self.lastmtime:
                flag = True
                self.lastmtime = os.path.getmtime(tifpath)
                #print 'mtime'+str(self.lastmtime)
            if os.path.getctime(tifpath) != self.lastctime:
                flag = True
                self.lastctime = os.path.getctime(tifpath)
                #print 'atime'+str(self.lastctime)
        return flag

if __name__ == '__main__':
    '''
    dirpath = '/Users/Mike/Downloads/1208NSLSX17A_LiRh2O4/'
    output = getTiffImages(dirpath)
    print output
    '''
