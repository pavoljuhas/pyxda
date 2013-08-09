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
import traitsui.api
import enable.api
import numpy as np
import Queue
import threading
import os

from traits.api import HasTraits, Instance, Int, List, Bool, Str

from display import Display
from controlpanel import ControlPanel, MetadataPanel
from image import Image, ImageCache
from loadthread import LoadThread

class ProcessCenter(HasTraits):
    '''Delegates tasks to the appropriate resources and stores data.

    Manages GUI events and decides who should handle them. Also, serves as the
    central data structure to store all of the information related to the 
    current data set.
    '''
    ##############################################
    # Initialize
    ##############################################
    def __init__(self, **kwargs):
        super(ProcessCenter, self).__init__()
        
        self.processing_job = threading.Thread(target=self.processJob)
        self.processing_job.daemon = True
        
        self.jobqueue = Queue.Queue()
        self.add_trait('display', Display(self.jobqueue))
        self.add_trait('datalist', List())
        self.add_trait('datalistlength', Int())
        self.add_trait('message', Str(''))
        self.add_trait('cache', Instance(ImageCache, ImageCache()))
        self.add_trait('pic', Instance(Image))
        self.add_trait('hasImage', Bool())

        self.on_trait_change(self.plotData, 'pic', dispatch='new')
        
        self.initDisplay()
        self.initData()
        return

    def initDisplay(self):
        '''Plots are initialized as None.

        This allows for consistency with the plot methods of the Display
        class. They will be created when these methods are called the first
        time.
        '''
        self.imageplot = None
        self.histogram = None
        self.plot1d = None
        return
    
    def initData(self):
        '''Initializes all values before a data set is chosen.

        This method is used both at start and when switching directories in 
        order to reset the display and internal mechanisms.
        '''
        del self.datalist[:]
        self.datalistlength = 0
        self.message = ''
        self.hasImage = False
        self.cache.clear()
        self.newndx = -1
        self.rrplots = {}

        pic = Image(-1, '')
        pic.data = np.zeros((2048, 2048))
        self.pic = pic
        self.plotData()
        return

    ##############################################
    # Jobs
    ##############################################
    def addNewImage(self, path, **kwargs):
        '''Adds a new image to the list of data in the directory.
        
        path -- the filepath of the image

        Warning: If there is no associated metadata file of the form
        path.metadata, then there is a message displayed.

            No metadata found for <filename>.
        '''
        #print 'Image Added:'
        n = len(self.datalist)
        self.datalist.append(Image(n, path))
        self.hasImage = True
        self.datalistlength += 1
        
        if not self.datalist[n].metadata:
            self.message = 'No metadata found for %s.' % os.path.split(path)[1]
            print self.message
        return
    
    def plotData(self):
        '''Updates the plots to display data related to the current image.'''
        #print 'Plot Data'
        self.pic.load()
        self.imageplot = self.display.plotImage(self.pic, self.imageplot)
        self.histogram = self.display.plotHistogram(self.pic, self.histogram)
        self.plot1d = self.display.plot1DCut(self.pic, self.plot1d)
        return

    def startLoad(self, dirpath):
        '''Creates a load thread to process the current directory.

        If a directory has already been chosen, the display will be reset
        first.
        '''
        #print 'Load Started'
        if self.hasImage == True:
            self.initData()
        self.loadimage = LoadThread(self.jobqueue, dirpath)
        self.loadimage.start()
        return

    def initCache(self):
        '''Initializes the cache by placing the first 2 images in the cache.'''
        #print 'Init Cache'
        self.pic = self.datalist[0]
        for i in range(2):
            pic = self.datalist[i]
            self.cache.append(pic)
            pic.load()
        return 

    def changeIndex(self, newndx):
        '''Determines how the new image selection should be processed.'''
        #print 'Change Index'
        self.newndx = newndx
        currentpos = self.pic.n

        if newndx - currentpos == -1:
            #print 'Click left'
            self.updateCache('left')
        elif newndx - currentpos == 1:
            #print 'Click right'
            self.updateCache('right')
        elif newndx - currentpos == 0:
            #print 'Click same'
            return
        elif newndx < self.datalistlength and newndx >= 0:
            #print 'Click skip'
            self.updateCache('click')
        return

    def updateCache(self, strnext):
        '''Updates the image cache based on the current image.

        strnext -- the type of traversal: either left, right, or click

        Warning: The following messages may be displayed based on error 
        checking of user input.

        Warning: No images loaded.
        Warning: Cannot traverse LEFT.
        Warning: Cannot traverse RIGHT.
        '''
        #print 'Update Cache'
        #print self.cache
        n = self.pic.n
        if n == -1:
            self.message = 'WARNING: No images loaded.'
            print self.message
            return
        if strnext == 'left':
            self.newndx = n - 1
            #print '%d -> %d' % (n, self.newndx)
            if n == 0:
                self.message = 'WARNING: Cannot traverse LEFT.'
                print self.message
                return
            else:
                self._innerCache(n, -1)
        elif strnext == 'right':
            self.newndx = n + 1
            #print '%d -> %d' % (n, self.newndx)
            if n == self.datalistlength - 1:
                self.message = 'WARNING: Cannot traverse RIGHT.'
                print self.message
                return
            else:
                self.cache.reverse()
                self._innerCache(n, 1)
                self.cache.reverse()
        elif strnext == 'click':
            #print '%d -> %d' % (n, self.newndx)
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
        #print self.cache
        return

    def _innerCache(self, n, i):
        '''Internal cache method that deals with cache logic when updating.'''
        self.pic = self.cache.popleft()

        self.cache.appendleft(self.pic)
        if (n > 1 and i == -1) or (n < self.datalistlength-2 and i == 1):
            pic = self.datalist[n+i*2]
            self.cache.appendleft(pic)

        if (n == 1 and i == -1) or (n == self.datalistlength-2 and i == 1):
            self.cache.pop()
        return

    # TODO: As more RRs are supported, move them to a separate file.
    def countLowPixels(self, image):
        '''Finds the percentage of pixels below the selected threshold.

        image -- Image object
        '''
        selection = self.display._selection
        data = image.ravel()
        limit = selection[0]
        count = np.count_nonzero(data < limit)
        rv = count/float(np.size(data))
        return rv*100

    def countHighPixels(self, image):
        '''Finds the percentage of pixels above the selected threshold.

        image -- Image object
        '''
        selection = self.display._selection
        data = image.ravel()
        limit = selection[1]
        count = np.count_nonzero(data > limit)
        rv = count/float(np.size(data))
        return rv*100

    def createRRPlot(self, rrchoice):
        '''Generates a new plot based on the RR given and the current data.

        rrchoice -- the reduced representation

            Warning: RR Plot Cannot be (Re)created
            Warning: No RR selected.
        '''
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

        elif rrchoice == '% Pixels Below Threshold':
            if self.display._selection != None:
                f = self.countLowPixels
            else:
                self.message = 'A range selection must be chosen.'
                print self.message
                return

        elif rrchoice == '% Pixels Above Threshold':
            if self.display._selection != None:
                f = self.countHighPixels
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

    ##############################################
    # Job Processing
    ##############################################
    def startProcessJob(self):
        '''Starts a thread to process tasks in the jobqueue.'''
        self.processing_job.start()
        return
    
    def processJob(self):
        '''Translates a job into the appropriate method calls.

        A job must be in the following form:
            ['task', [kwargs]] 
        '''
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
            elif jobtype == 'initcache':
                self.initCache()
            elif jobtype == 'plotrr':
                self.createRRPlot(*kwargs)
            elif jobtype == 'changendx':
                self.changeIndex(*kwargs)
            elif jobtype == 'startload':
                self.startLoad(*kwargs)
            elif jobtype == 'updatecmap':
                self.display.updateColorMap(*kwargs)
            elif jobtype == 'updatemsg':
                self.message = jobdata[1]
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
