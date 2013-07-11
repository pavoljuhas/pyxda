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
from controlpanel import ControlPanel
from imagecontainer import ImageContainer, ImageCache
from loadimages import LoadImage

# Major library imports
from numpy import linspace, meshgrid, pi
from scipy.special import jn

from controlpanel import ControlPanel

class PyXDA(HasTraits):

    ##############################################
    # Initialize
    ##############################################
    def __init__(self, **kwargs):
        super(PyXDA, self).__init__()
        
        self.processing_job = threading.Thread(target=self.processJob)
        self.processing_job.daemon = True
        
        self.datalist = []
        self.add_trait('datalistlength', Int(0))
        
        self.on_trait_change(self.plotData, 'plotnow', dispatch='ui')
        self.on_trait_change(self.datalistLengthAdd,'datalistlengthadd', dispatch='ui')
        
        self.initLoadimage()
        self.initDisplay()
        self.initControlPanel()
        self.initCMap()

        return
    
    def initLoadimage(self):
        self.jobqueue = Queue.Queue()
        #self.loadimage = LoadImage(self.jobqueue)
        self.add_trait('datalist', List())
        self.imagecache = ImageCache()
        pic = np.zeros((2048, 2048))
        self.add_trait('pic', Instance(np.ndarray, pic))
        title = '2D Image'
        self.add_trait('title', title)
        self.add_trait('hasImage', Bool(False))
        return

    def initDisplay(self):
        self.add_trait('display', Display())
        self.add_trait('imageplot', Instance(Plot, self.display.plotImage(self.pic, 
                                            self.title, None)))
        self.imageplot.x_axis.visible = False
        self.imageplot.y_axis.visible = False
        
        #Second Plot
        self.add_trait('imageplot2', Instance(Plot, self.display2.plotImage(self.pic, '', None)))
        self.imageplot2.x_axis.visible = False
        self.imageplot2.y_axis.visible = False
        
        return

    def initControlPanel(self):
        self.panel = ControlPanel(display=self.display)
        return

    def initCMap(self):
        self.hascmap = False
        mapdata = np.zeros((12, 12))
        self.add_trait('mapdata', Instance(np.ndarray, mapdata))
        self.add_trait('cmap', Instance(Plot, self.display.plotImage(self.mapdata,
                                        'Total Intensity Map', None)))

    ##############################################
    # Tasks  
    ##############################################
    def addNewImage(self, imagename, **kwargs):
        '''add new image and create jobs to process new image
        image:    2d ndarray, new 2d image array
        '''
        listn = len(self.datalist)
        self.datalist.append(ImageContainer(listn, imagename, self.loadimage.dirpath))
        self.hasImage = True
        self.jobqueue.put(['datalistlengthadd'])
        #print 'Image Added'
        return
   
    plotnow = Event
    def plotData(self):
        self.imageplot = self.display.plot2DImage(self.pic, self.imageplot, self.title)
        #print 'Plot Data'
        return

    datalistlengthadd = Event
    def datalistLengthAdd(self):
        '''add datalistlength by 1, only use this method to modify the datalistlength
        otherwise there will be some problem of frame range in UI
        '''
        self.datalistlength = self.datalistlength + 1
        #print 'DataListLengthAdd'
        return

    def startLoad(self, dirpath):
        if self.hasImage == True:
            self.resetViewer()
        self.loadimage = LoadImage(self.jobqueue, dirpath)
        self.loadimage.start()
        
    def initCache(self):
        for i in range(2):
            if i == 0:
                self.pic = self.loadimage.getImage(self.datalist[i])
                self.title = self.datalist[i].imagename
                self.plotnow = {}
            self.imagecache.cache.append(self.loadimage.getImage(self.datalist[i]))
        self.imagecache.imagepos = 0
        #print 'Init Cache'
        return 

    def changeIndex(self):
        #print 'Change Index'
        n = self.display.ndx[0] + (11 - self.display.ndx[1])*12
        time.sleep(0.5)
        #print n

        if self.hascmap == False:
            return
        
        currentpos = self.imagecache.imagepos
        if n - currentpos == -1:
            #print 'Click left'
            self.updateCache('left') 
        elif n - currentpos == 1:
            #print 'Click right'
            self.updateCache('right')
        elif n - currentpos == 0:
            #print 'Click same'
            return
        elif n < self.datalistlength and n >= 0:
            #print 'Click skip'
            self.newndx = n
            self.updateCache('click')
        return

    def updateCache(self, strnext):
        n = self.imagecache.imagepos
        #print 'Update Cache'
        #print n
        if n == -1:
            print 'Cannot traverse ' + strnext
            return
        if strnext == 'left':
            if n == 0:
                return
            else:
                self._innerCache(n, -1)
                return
        elif strnext == 'right':
            if n == self.datalistlength - 1:
                return
            else:
                self.imagecache.cache.reverse()
                self._innerCache(n, 1)
                self.imagecache.cache.reverse()
                return
        elif strnext == 'click':
            cache = self.imagecache
            cache.cache.clear()
            if self.newndx == 0:
                self.initCache()
                return

            cache.imagepos = self.newndx
            for i in range(2):
                n = self.newndx - i
                self.pic = self.loadimage.getImage(self.datalist[n])
                self.title = self.datalist[n].imagename
                if i == 0:
                    self.plotnow = {}
                cache.cache.appendleft(self.pic)
            if not self.newndx == self.datalistlength - 1:
                temp = self.datalist[self.newndx+1]
                cache.cache.append(self.loadimage.getImage(temp))
        return

    def _innerCache(self, n, i):
        self.pic = self.imagecache.cache.popleft()
        self.title = self.datalist[n+i*1].imagename
        self.plotnow = {}

        self.imagecache.cache.appendleft(self.pic)
        if (n > 1 and i == -1) or (n < self.datalistlength-2 and i == 1):
            cont = self.datalist[n+i*2]
            self.imagecache.cache.appendleft(self.loadimage.getImage(cont))

        if (n == 1 and i == -1) or (n == self.datalistlength-2 and i == 1):
            self.imagecache.cache.pop()

        self.imagecache.imagepos = self.imagecache.imagepos + i*1
        return

    def createCMap(self):
        if self.datalistlength == 0 or self.hascmap == True:
            print 'Intensity Map Already Generated.......'
            return
        print 'Generating Intensity Map........'
        for i, cont in enumerate(self.datalist):
            data = self.loadimage.getImage(cont)
            print '%d: %s........Loaded' % (i, cont.imagename)
            self.mapdata[11-i/12, i%12] = data.sum()
            if (i+1) % 5 == 0:
                self.cmap = self.display.plot2DImage(self.mapdata, 
                                        self.cmap, 'Total Intensity Map')
        self.cmap = self.display.plot2DImage(self.mapdata, 
                                    self.cmap, 'Total Intensity Map')
        self.hascmap = True
        print 'Loading Complete'
        return

    def resetViewer(self):
        #print 'Reset'
        if self.hasImage == False:
            return

        #self.pic = np.zeros((2048, 2048))
        #self.title = '2D Image'
        #self.imageplot = self.display.plotImage(self.pic, self.title, self.imageplot)
        #self.plotnow = {}

        self.mapdata = np.zeros((12, 12))
        self.cmap = self.display.plotImage(self.mapdata, 'Total Intensity Map', 
                                                                self.cmap)
        self.hascmap = False
        self.hasImage = False

        with self.jobqueue.mutex:
            self.jobqueue.queue.clear()
        
        del self.datalist[:]
        self.datalistlength = 0
        self.imagecache.clean()
        #del self.loadimage.filelist[:]
       
        return


    ##############################################
    # Job Processing
    ##############################################
    def startProcessJob(self):
        '''Call processImage thread and start image processing. This 
        method should be called before the imageload thread.
        '''
        self.processing_job.start()
        #self.jobqueue.put(['updateconfig'])
        return
    
    def processJob(self):
        while True:
            #retrieve job data
            jobdata = self.jobqueue.get(block=True)
            jobtype = jobdata[0]
            kwargs = jobdata[1] if len(jobdata)==2 else {}
            
            #deal with different jobs
            '''
            self.pdfliveconfig.lockPanel()
            if jobtype == 'lock':
                self.pdfliveconfig.lockPanel()
            elif jobtype == 'release':
                self.pdfliveconfig.releasePanel()
            '''
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
            elif jobtype == 'createcmap':
                self.createCMap()
            elif jobtype == 'changendx':
                self.changeIndex()
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
