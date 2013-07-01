# EDIT IMPORTS AT END
import chaco.api
from enthought.traits.api import HasTraits, Instance, Dict
from chaco.api import ArrayPlotData, Plot, jet
import traitsui.api
import enable.api
import numpy as np
import scipy as sp
import fabio

from display import Display
from ui_pyxda import ControlPanel


class PyXDA(HasTraits):

    
    
    def __init__(self, **kwargs):
        super(PyXDA, self).__init__()
        '''
        self.processing_job = threading.Thread(target=self.processJob)
        self.processing_job.daemon = True
        self.datalist = []
        '''
        self.add_trait('images', {})
        self.initDisplay()
        self.initControlPanel()
        return

    def initDisplay(self):
        self.display = Display()
        pic = np.zeros((2048, 2048))
        self.add_trait('pic', Instance(np.ndarray, pic))
        self.add_trait('imageplot', Instance(Plot, self.display.plotImage(self.pic, 
                                            '2D image', None)))
        return

    def initControlPanel(self):
        self.panel = ControlPanel(display=self.display)
        return


    ##############################################
    #   Plot methods
    ##############################################
    def plotData(self, plot, title):
        self.imageplot = self.display.plot2DImage(plot, self.imageplot, title)
        return


if __name__ == '__main__':
    PyXDA().configure_traits()
