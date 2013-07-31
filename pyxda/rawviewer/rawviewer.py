#!/usr/bin/env python

# EDIT IMPORTS AT END
import chaco.api
from enthought.traits.api import HasTraits, Instance, \
                                Dict, Event, Int, List, Bool, String
from chaco.api import ArrayPlotData, Plot, jet
import traitsui.api
import enable.api
import numpy as np
import scipy as sp
import fabio
import Queue
import threading
import time

from display import Display
from controlpanel import ControlPanel, MetadataPanel
from imagecontainer import Image, ImageCache
from loadimages import LoadImage

####################

SIZE = 12

####################

class RawViewer(HasTraits):
    
    ##############################################
    # Initialize
    ##############################################
    def __init__(self, **kwargs):
        super(RawViewer, self).__init__()
        
        self.processing_job = threading.Thread(target=self.processJob)
        self.processing_job.daemon = True
        
        self.jobqueue = Queue.Queue()
        self.add_trait('datalist', List())
        self.add_trait('datalistlength', Int(0))
        
        self.on_trait_change(self.plotData, 'pic', dispatch='new')
        self.on_trait_change(self.datalistLengthAdd,'datalistlengthadd', dispatch='ui')
       
        self.initLoadimage()
        self.initDisplay()
        self.initCMap()
        return
    
    def initLoadimage(self):
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
        self.add_trait('plot1d', Instance(Plot,
                                        self.display.plotHistogram(self.pic)))
        self.plot1d.value_axis.title = "1D Cut"
        self.add_trait('histogram', Instance(Plot,
                                        self.display.plotHistogram(self.pic)))
        self.newndx = -1
        return
    
    # TODO: Update
    def initCMap(self):
        self.hascmap = False
        #TODO
        #self.add_trait('rrplot', Instance(Plot, 
        #                        self.display.plotRRMap(None, None)))
        self.rrplots = {}

    ##############################################
    # Tasks  
    ##############################################
    def addNewImage(self,path, **kwargs):
        '''add new image and create jobs to process new image
        image:    2d ndarray, new 2d image array
        '''
        print 'Image Added'
        listn = len(self.datalist)
        self.datalist.append(Image(listn, path))
        self.hasImage = True
        self.jobqueue.put(['datalistlengthadd'])
        return
   
    
    def plotData(self):
        print 'Plot Data'
        self.pic.load()
        self.imageplot = self.display.plotImage(self.pic, self.imageplot)
        #TODO
        self.histogram = self.display.plotHistogram(self.pic, self.histogram)
        self.plot1d = self.display.plotHistogram(self.pic, None)
        return

    # TODO
    datalistlengthadd = Event
    def datalistLengthAdd(self):
        '''add datalistlength by 1, only use this method to modify the datalistlength
        otherwise there will be some problem of frame range in UI
        '''
        #print 'DataListLengthAdd'
        self.datalistlength += 1
        return

    def startLoad(self, dirpath):
        print 'Load Started'
        if self.hasImage == True:
            self.resetViewer()
        self.loadimage = LoadImage(self.jobqueue, dirpath)
        self.loadimage.start()
    
    # TODO: not as important
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

        #if self.hascmap == False:
        #    return
        
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
            print 'Cannot traverse ' + strnext
            return
        if strnext == 'left':
            self.newndx = n - 1
            print '%d -> %d' % (n, self.newndx)
            if n == 0:
                return
            else:
                self._innerCache(n, -1)
        elif strnext == 'right':
            self.newndx = n + 1
            print '%d -> %d' % (n, self.newndx)
            if n == self.datalistlength - 1:
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
                if self.newndx is not self.datalistlength - 1:
                    self.cache.append(self.datalist[self.newndx+1])
                else:
                    self.cache.append(Image(-1, ''))

            '''
                for i in range(2):
                    n = self.newndx - i
                    pic = self.datalist[n]
                    self.cache.appendleft(pic)
                    if i == 0:
                        self.pic = pic
                        self.plotnow = {}
                if self.newndx is not self.datalistlength - 1:
                    temp = self.datalist[self.newndx+1]
                    self.cache.append(temp)
                else:
                    self.cache.append(Image(-1, ''))
            '''
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

    def createRRPlot(self, rrchoice):
        if self.datalistlength is 0 or self.hascmap is True:
            print 'Intensity Map Cannot be (Re)created.......'
            return
        elif rrchoice == 'Choose a Reduced Representation':
            return

        if rrchoice == 'Mean':
            f = lambda x: np.mean(x)

        elif rrchoice == 'Total Intensity':
            f = lambda x: np.sum(x)

        elif rrchoice == 'Standard Deviation':
            f = lambda x: np.std(x)

        elif rrchoice == 'Pixels Above Upper Bound':
            return

        elif rrchoice == 'Pixels Below Lower Bound':
            return

        if rrchoice not in self.rrplots:
            self.rrplots[rrchoice] = rrplot = self.display.plotRRMap(None, rrchoice, None)
        else:
            return

        print 'Generating Intensity Map........'
        for i, image in enumerate(self.datalist):
            image.load()
            print '%d: %s........Loaded' % (i, image.name)
            rr = f(image.data)
            rrplot = self.display.plotRRMap(rr, rrchoice, rrplot)
            image.data = None

        #self.hascmap = True
        print 'Loading Complete'
        return

    def resetViewer(self):
        print 'Reset'
        if self.hasImage == False:
            return

        #self.mapdata = np.zeros((SIZE, SIZE))
        self.rrplots = {}
        #self.rrplot = self.display.plotImage(None, 'Total Intensity Map')
        self.hascmap = False
        self.hasImage = False
        self.newndx = -1

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
            #retrieve job data
            jobdata = self.jobqueue.get(block=True)
            jobtype = jobdata[0]
            kwargs = jobdata[1] if len(jobdata)==2 else {}
            
            #deal with different jobs
            if jobtype == 'newimage':
                self.addNewImage(**kwargs)
            elif jobtype == 'updatecache':
                self.updateCache(*kwargs)
            elif jobtype == 'plotdata':
                self.plotnow = kwargs
            elif jobtype == 'datalistlengthadd':
                self.datalistlengthadd = True
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