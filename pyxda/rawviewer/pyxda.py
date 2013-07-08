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

from display import Display
from ui_pyxda import ControlPanel
from imagecontainer import ImageContainer, ImageCache
from loadimages import LoadImage

class PyXDA(HasTraits):

    ##############################################
    # Initialize
    ##############################################
    def __init__(self, **kwargs):
        super(PyXDA, self).__init__()
        
        self.processing_job = threading.Thread(target=self.processJob)
        self.processing_job.daemon = True
        
        self.datalist = []
        self.add_trait('images', {})
        self.add_trait('datalistlength', Int(0))
        
        self.on_trait_change(self.plotData, 'plotnow', dispatch='ui')
        self.on_trait_change(self.datalistLengthAdd,'datalistlengthadd', dispatch='ui')
        
        self.initLoadimage()
        self.initDisplay()
        self.initControlPanel()
        return
    
    def initLoadimage(self):
        self.jobqueue = Queue.Queue()
        self.loadimage = LoadImage(self.jobqueue)
        self.add_trait('datalist', List())
        self.imagecache = ImageCache()
        pic = np.zeros((2048, 2048))
        self.add_trait('pic', Instance(np.ndarray, pic))
        title = '2D Image'
        self.add_trait('title', title)
        self.add_trait('hasimage', Bool(False))
        return

    def initDisplay(self):
        self.display = Display()
        self.display2 = Display()
        
        #First Plot
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


    ##############################################
    # Tasks  
    ##############################################
    def addNewImage(self, imagename, **kwargs):
        '''add new image and create jobs to process new image
        image:    2d ndarray, new 2d image array
        '''
        #self.jobqueue.put(['lock'])
        listn = len(self.datalist)
        self.datalist.append(ImageContainer(listn, imagename, self.loadimage.dirpath))
        self.hasimage = True
        self.jobqueue.put(['datalistlengthadd'])
        print 'Image Added'
        return
   
    plotnow = Event
    def plotData(self):
        self.imageplot = self.display.plot2DImage(self.pic, self.imageplot, self.title)
        print 'Plot Data'
        return

    datalistlengthadd = Event
    def datalistLengthAdd(self):
        '''add datalistlength by 1, only use this method to modify the datalistlength
        otherwise there will be some problem of frame range in UI
        '''
        self.datalistlength = self.datalistlength + 1
        print 'DataListLengthAdd'
        return

    def processExistingFiles(self):
        filelist = self.loadimage.filelist
        for filen in filelist:
            self.jobqueue.put(['newimage', {'imagename':filen}])
        print 'Process Existing Files'
        return

    def initCache(self):
        for i in range(2):
            if i == 0:
                self.pic = self.loadimage.getImage(self.datalist[i])
                self.title = self.datalist[i].imagename
            self.imagecache.cache.append(self.loadimage.getImage(self.datalist[i]))
        self.imagecache.imagepos = 0
        print 'Init Cache'
        return 

    def updateCache(self, strnext):
        n = self.imagecache.imagepos
        print 'Update Cache'
        print n
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

        '''
        if strnext == 'left':
            if n == 0:
                return
            elif n == 1:
                self.pic = self.imagecache.cache.popleft()
                self.title = self.datalist[n-1].imagename
                self.imagecache.cache.pop()
                self.plotnow = {}
                self.imagecache.imagepos -= 1
                self.imagecache.cache.append(temp)
                return
            else:
                cont = self.datalist[n-2]
                self.pic = self.imagecache.cache.popleft()
                self.title = cont.imagename
                self.plotnow = {}
                self.imagecache.cache.pop()
                self.imagecache.cache.appendleft(self.loadimage.getImage(cont))
                self.imagecache.imagepos -= 1
                self.imagecache.cache.append(temp)
                return
        elif strnext == 'right':
            if n == self.datalistlength - 1:
                return
            elif n == self.datalistlength - 2:
                self.pic = self.imagecache.cache.pop()
                self.title = self.datalist[n+1].imagename
                self.imagecache.cache.popleft()
                self.plotnow = {}
                self.imagecache.imagepos += 1
                self.imagecache.appendleft(temp)
                return
            else:
                cont = self.datalist[n+2]
                self.pic = self.imagecache.cache.pop()
                self.title = cont.imagename
                self.plotnow = {}
                print self.imagecache.cache
                
                self.imagecache.cache.popleft()
                self.imagecache.cache.append(self.loadimage.getImage(cont))
                self.imagecache.imagepos += 1
                self.imagecache.cache.append(temp)
                return
        '''

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
            elif jobtype == 'processexist':
                self.processExistingFiles()
            #self.pdfliveconfig.releasePanel()
            jobdata = []
            self.jobqueue.task_done()
        return

def main():
    a = PDFlive()
    a.startProcessJob()
    a.loadimage.initLive()
    a.loadimage.start()
    return
    
if __name__=='__main__':
    main()
