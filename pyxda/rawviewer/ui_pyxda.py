from loadimages import getTiffImages
from enthought.traits.api import HasTraits, Instance
from display import Display
from enthought.traits.ui.api import View,Item, Group, HSplit, Handler
from traits.api import *
from enable.api import ComponentEditor,Component
from enthought.traits.ui.menu import NoButtons
from chaco.api import ArrayPlotData, Plot, jet, GridContainer

import pyxda as px
from handler import PyXDAHandler

class Camera(HasTraits):
    gain = Enum(1, 2, 3, )
    exposure = CInt(10, label="Exposure")

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    display = Display()
    load_data = Button('Load Data')
    camera = Instance(Camera)

    view = View(
            Group(
                Item('load_data', show_label=False),
                Item('camera', style='custom', show_label=False)
                )
            )

    def _camera_default(self):
        self.camera = Camera()

class PyXDAUI(HasTraits):
    
    imageplot = Instance(Plot)

    def __init__(self):
        super(PyXDAUI, self).__init__()
        #TODO: Initializes the UI
        self.add_trait('pyxda', px.PyXDA())
        self.add_trait('panel', self.pyxda.panel)
        self.add_trait('display', self.pyxda.display)

        self.imagecontainer = Instance(Component)
        self.updateImageContainer()

    # TODO: Adjust view
    view = View(HSplit(Item('imagecontainer', editor=ComponentEditor(),
                            dock='vertical'),
                       Item('panel', style="custom"),
                       show_labels=False,
                      ),
                resizable=True,
                height=0.75, width=0.75,
                handler=PyXDAHandler(),
                buttons=NoButtons)

    #############################
    # UI Action Handling
    #############################

    @on_trait_change('pyxda.images')
    def imagesChanged(self):
        #TODO: Should definitely be modified.
        pic = self.pyxda.images.values()[0].data
        title = self.pyxda.images.keys()[0]
        self.pyxda.imageplot = self.pyxda.plotData(pic, title)
        
       #self.updateImageContainer()

        return
  
    # TODO: whatever the panel's name is
    @on_trait_change('panel.load_data', post_init=True)
    def _load_data_fired(self):
        '''Loads data for display.'''
        # TODO: Needs to be updated for scaleability.
        dirpath = '/Users/Mike/Downloads/1208NSLSX17A_LiRh2O4/'
        self.pyxda.images = getTiffImages(dirpath)

        return


    def updateImageContainer(self):
            
        container = GridContainer(bgcolor="lightgray", shape=(1,1), 
                                    use_backbuffer=True)
        self.imagecontainer = container

        cont = getattr(self.pyxda, 'imageplot')
        if cont in container._components:
            container.remove(cont)
        
        container.add(cont)
        
        container.get_preferred_size()
        container.invalidate_draw()
        return






if __name__ == '__main__':
    ui = PyXDAUI()
    ui.configure_traits()
    
    '''
    panel = ControlPanel(camera=Camera(), display=Display())
    panel.configure_traits()
    '''
