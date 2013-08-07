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

import chaco.api
from enthought.traits.api import HasTraits, Instance, \
                                Dict, Event, Int, List, Bool, String, Str
from chaco.api import ArrayPlotData, Plot, jet
import traitsui.api
import enable.api
import numpy as np
import scipy as sp
import fabio
import Queue
import threading
import time
import os

from display import Display
from controlpanel import ControlPanel, MetadataPanel
from image import Image, ImageCache
from loadimages import LoadImage

class ProcessCenter(HasTraits):
    
    ##############################################
    # Initialize
    ##############################################
    def __init__(self, **kwargs):
        super(ProcessCenter, self).__init__()
        
        self.processing_job = threading.Thread(target=self.processJob)
        self.processing_job.daemon = True
        
        self.jobqueue = Queue.Queue()
        self.add_trait('datalist', List())
        self.add_trait('datalistlength', Int(0))
        self.add_trait('message', Str(''))
        
        self.on_trait_change(self.plotData, 'pic', dispatch='new')
       
        self.initLoadImage()
        self.initDisplay()
        self.initCMap()
        return
    
    def initLoadImage(self):
        self.cache = ImageCache()
        self.add_trait('pic', Instance(Image, Image(-1, '')))
        self.pic.data = np.zeros((2048, 2048))
        self.add_trait('hasImage', Bool(False))
        return

    def initDisplay(self):
        self.add_trait('display', Display(self.jobqueue))
        # TODO: Move to Display.
        self.add_trait('imageplot', Instance(Plot, 
                                        self.display.plotImage(self.pic)))
        self.add_trait('histogram', Instance(Plot,
                                        self.display.plotHistogram(self.pic)))
        self.add_trait('plot1d', Instance(Plot,
                                        self.display.plot1DCut(self.pic)))
        self.newndx = -1
        return
    
    # TODO: Update
    def initCMap(self):
        self.rrplots = {}

    ##############################################
    # Tasks  
    ##############################################
    def addNewImage(self,path, **kwargs):
        '''add new image and create jobs to process new image
        image:    2d ndarray, new 2d image array
        '''
        print 'Image Added:'
        n = len(self.datalist)
        self.datalist.append(Image(n, path))
        self.hasImage = True
        self.datalistlength += 1
        
        if not self.datalist[n].metadata:
            self.message = 'No metadata found for %s.' % os.path.split(path)[1]
            print self.message
        return
    
    def plotData(self):
        print 'Plot Data'
        self.pic.load()
        self.imageplot = self.display.plotImage(self.pic, self.imageplot)
        #TODO
        self.histogram = self.display.plotHistogram(self.pic, self.histogram)
        self.plot1d = self.display.plot1DCut(self.pic, self.plot1d)
        return

    def startLoad(self, dirpath):
        print 'Load Started'
        if self.hasImage == True:
            self.resetViewer()
        self.loadimage = LoadImage(self.jobqueue, dirpath)
        self.loadimage.start()
        return

    def initCache(self):
        print 'Init Cache'
        self.pic = self.datalist[0]
        for i in range(2):
            pic = self.datalist[i]
            self.cache.append(pic)
            pic.load()
        return 

    def changeIndex(self, newndx):
        print 'Change Index'
        self.newndx = newndx

        currentpos = self.pic.n

        if newndx - currentpos == -1:
            print 'Click left'
            self.updateCache('left')
        elif newndx - currentpos == 1:
            print 'Click right'
            self.updateCache('right')
        elif newndx - currentpos == 0:
            print 'Click same'
            return
        elif newndx < self.datalistlength and newndx >= 0:
            print 'Click skip'
            self.updateCache('click')
        return

    def updateCache(self, strnext):
        print 'Update Cache'
        print self.cache
        n = self.pic.n
        if n == -1:
            self.message = 'WARNING: No images loaded.'
            print self.message
            return
        if strnext == 'left':
            self.newndx = n - 1
            print '%d -> %d' % (n, self.newndx)
            if n == 0:
                self.message = 'WARNING: Cannot traverse LEFT.'
                print self.message
                return
            else:
                self._innerCache(n, -1)
        elif strnext == 'right':
            self.newndx = n + 1
            print '%d -> %d' % (n, self.newndx)
            if n == self.datalistlength - 1:
                self.message = 'WARNING: Cannot traverse RIGHT.'
                print self.message
                return
            else:
                self.cache.reverse()
                self._innerCache(n, 1)
                self.cache.reverse()
        elif strnext == 'click':
            print '%d -> %d' % (n, self.newndx)
            self.cache.clear()
            if self.newndx == 0:
                self.initCache()
            else:
                self.pic = self.datalist[self.newndx]
                self.cache.append(self.datalist[self.newndx-1])
                self.cache.append(self.pic)
                if self.newndx != self.datalistlength - 1:
                    self.cache.append(self.datalist[self.newndx+1])
                else:
                    self.cache.append(Image(-1, ''))
        print self.cache
        return

    def _innerCache(self, n, i):
        self.pic = self.cache.popleft()

        self.cache.appendleft(self.pic)
        if (n > 1 and i == -1) or (n < self.datalistlength-2 and i == 1):
            pic = self.datalist[n+i*2]
            self.cache.appendleft(pic)

        if (n == 1 and i == -1) or (n == self.datalistlength-2 and i == 1):
            self.cache.pop()
        return

    def countDeadPixels(self, image):
        selection = self.display._selection
        data = image.ravel()
        limit = selection[0]
        count = np.count_nonzero(data < limit)
        rv = count/float(np.size(data))
        return rv*100

    def countSatPixels(self, image):
        selection = self.display._selection
        data = image.ravel()
        limit = selection[1]
        count = np.count_nonzero(data > limit)
        rv = count/float(np.size(data))
        return rv*100

    def createRRPlot(self, rrchoice):
        if self.datalistlength == 0:
            self.message = 'WARNING: RR Plot Cannot be (Re)created'
            print self.message
            return
        elif rrchoice == 'Choose a Reduced Representation':
            self.message = 'WARNING: No RR selected.'
            print self.message
            return

        if rrchoice == 'Mean':
            f = lambda x: np.mean(x)

        elif rrchoice == 'Total Intensity':
            f = lambda x: np.sum(x)

        elif rrchoice == 'Standard Deviation':
            f = lambda x: np.std(x)

        elif rrchoice == 'Percentage of Dead Pixels':
            if self.display._selection != None:
                f = self.countDeadPixels
            else:
                self.message = 'A range selection must be chosen.'
                print self.message
                return

        elif rrchoice == 'Percentage of Saturated Pixels':
            if self.display._selection != None:
                f = self.countSatPixels
            else:
                self.message = 'A range selection must be chosen.'
                print self.message
                return

        if rrchoice not in self.rrplots:
            self.rrplots[rrchoice] = rrplot = self.display.plotRRMap(
                                                np.array([0]), rrchoice, None)
        else:
            return
        
        rrdata = np.array([])
        self.message = 'Generating RR Plot........'
        print self.message
        for i, image in enumerate(self.datalist):
            image.load()
            self.message = '%d: %s........Loaded' % (i+1, image.name)
            print self.message
            rr = f(image.data)
            rrdata = np.append(rrdata, rr)
            rrplot = self.display.plotRRMap(rrdata, rrchoice, rrplot)
            image.data = None

        self.message = 'Loading Complete.'
        print self.message
        return

    def resetViewer(self):
        print 'Reset'

        self.rrplots = {}
        self.hasImage = False
        self.newndx = -1
        self.message = ''
        img = Image(-1, '')
        img.data = np.zeros((2048, 2048))
        self.pic = img

        with self.jobqueue.mutex:
            self.jobqueue.queue.clear()
        
        self.cache.clear()
        del self.datalist[:]
        self.datalistlength = 0
        return


    ##############################################
    # Job Processing
    ##############################################
    def startProcessJob(self):
        '''Call processImage thread and start image processing. This 
        method should be called before the imageload thread.
        '''
        self.processing_job.start()
        return
    
    def processJob(self):
        while True:
            # retrieve job data
            jobdata = self.jobqueue.get(block=True)
            jobtype = jobdata[0]
            kwargs = jobdata[1] if len(jobdata)==2 else {}
            
            # deal with different jobs
            if jobtype == 'newimage':
                self.addNewImage(**kwargs)
            elif jobtype == 'updatecache':
                self.updateCache(*kwargs)
            elif jobtype == 'plotdata':
                self.plotnow = kwargs
            elif jobtype == 'initcache':
                self.initCache()
            elif jobtype == 'plotrr':
                self.createRRPlot(*kwargs)
            elif jobtype == 'changendx':
                self.changeIndex(*kwargs)
            elif jobtype == 'reset':
                self.resetViewer()
            elif jobtype == 'startload':
                self.startLoad(*kwargs)
            elif jobtype == 'updatecmap':
                self.display.updateColorMap(*kwargs)
            elif jobtype == 'updatemsg':
                self.message = jobdata[1]
            jobdata = []
            self.jobqueue.task_done()
        return

def main():
    a = PyXDA()
    a.startProcessJob()
    a.loadimage.initLive()
    a.loadimage.start()
    return
    
if __name__=='__main__':
    main()
