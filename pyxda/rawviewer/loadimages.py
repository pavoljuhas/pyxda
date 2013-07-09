# -*- coding: utf-8-sig -*-
import os
import numpy as np
import re
import fabio
import time
from enthought.traits.api import Dict, Instance, Directory, HasTraits
import threading


class LoadImage(HasTraits, threading.Thread):


    def __init__(self, queue):
        threading.Thread.__init__(self)
        super(LoadImage, self).__init__() 

        self.add_trait('dirpath', Directory())
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
                dirlist = os.listdir(self.dirpath)
                for f in dirlist:
                    if f[-4:] == "tiff" or f[-3:] == "tif":
                        self.filelist.append(f)
                break
            else:
                print 'Directory does not exist. (LoadImage)'

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
            
            if self.checkTime(self.tifdirectory):
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
            self.jobqueue.put(['newimage', {'imagename':self.filelist[i]}])
            print 'Image Process Sent'
            
        self.jobqueue.put(['initcache'])
        self.jobqueue.put(['plotdata'])
        return

    def getImage(self, imagecontainer):
        '''return 2d ndarray image array'''
        fo = fabio.open(imagecontainer.imagepath)
        return fo.data

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

