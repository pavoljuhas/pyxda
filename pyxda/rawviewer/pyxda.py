from enthought.traits.api import HasTraits,Int,Float,Str,Property, on_trait_change, Directory
from enthought.traits.api import Range,Array, Instance
from enthought.traits.ui.api import View,Item,Label, HSplit, Handler
from enthought.traits.ui.menu import NoButtons
from chaco.api import Plot, ArrayPlotData
from chaco import default_colors as dc
from enable.component_editor import ComponentEditor
import numpy as np
import fabio

from display import Display
from ui_pyxda import ControlPanel
from handler import PyXDAHandler
from loadimages import getTiffImages

class PyXDA(HasTraits):
    
    images = {}
    path = Directory()

    def __init__(self, **kwargs):
        super(PyXDA, self).__init__()
        '''
        self.processing_job = threading.Thread(target=self.processJob)
        self.processing_job.daemon = True
        self.datalist = []
        '''
        self.initDisplay()
        self.initControlPanel()
        return
    
    def initDisplay(self):
        #TODO: Make it not hard coded
        self.display = Display()
        
        dirpath = 'C:\\Users\\Mark\\Images\\1208NSLSX17A_LiRh2O4\\'
        self.images = getTiffImages(dirpath)

        #pic = np.zeros((2048, 2048))
        pic = self.images.values()[0].data

        self.add_trait('pic', Instance(np.ndarray, pic))
        self.add_trait('imageplot', Instance(Plot, self.display.plotImage(self.pic, 
                                             '1/10'+self.images.keys()[0], None)))
        return

    def initControlPanel(self):
        #TODO: Should NOT pass itself to control panel
        self.add_trait('panel', Instance(ControlPanel,
                                    ControlPanel(display=self.display, pyxda=self)))
        return

    view = View(HSplit(Item('imageplot', editor=ComponentEditor()),
                       Item('panel', style="custom"),
                       show_labels=False
                      ),
                resizable=True,
                height=0.75, width=0.75,
                handler=PyXDAHandler(),
                buttons=NoButtons)

    def updatePlot(self, index):
        #TODO: Should definitely be modified.
        pic = self.images.values()[index].data
        self.display.plotImage(pic, str(index+1)+'/10'+self.images.keys()[index], self.imageplot)

if __name__ == '__main__':
    PyXDA().configure_traits()
