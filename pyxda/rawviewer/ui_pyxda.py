from enthought.traits.api import HasTraits, Instance
from display import Display
from enthought.traits.ui.api import View,Item, Group, HGroup, HSplit, Handler, VSplit, VGroup
from traits.api import *
from enable.api import ComponentEditor,Component
from enthought.traits.ui.menu import NoButtons
from chaco.api import ArrayPlotData, Plot, jet, GridContainer

import pyxda as px
from handler import PyXDAHandler

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    #Traits for this class
    display = Display()
    dirPath = Directory()
    left_arrow = Button('<')
    right_arrow = Button('>')
    reset = Button('Reset')
    quality = Button('Quality Assessment')

    #GUI for this panel
    view = View(
               Group(
                   Item('dirPath', label = "Folder Path"),
                   HGroup(
                       Item('left_arrow', label = "Image"), 
                       Item('right_arrow', show_label = False),
                       Item('reset', show_label = False)
                   ),
                   Item('quality', show_label = False),
                   show_border = True,
                   label = 'Controls'
               )
           )

class PyXDAUI(HasTraits):
    
    imageplot = Instance(Plot)

    def __init__(self):
        super(PyXDAUI, self).__init__()
        #TODO: Initializes the UI
        self.add_trait('pyxda', px.PyXDA())
        self.add_trait('panel', self.pyxda.panel)
        self.add_trait('display', self.pyxda.display)
        self.pyxda.startProcessJob()
        self.pyxda.loadimage.start()


        self.imagecontainer = Instance(Component)
        self.updateImageContainer()

    # TODO: Adjust view
    view = View(HSplit(Item('imagecontainer', editor=ComponentEditor(),
                            dock='vertical'),
                           Item('panel', style="custom", show_label = False),
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

    @on_trait_change('panel.dirPath', post_init=True)
    def _load_data_fired(self):
        '''Loads data for display.'''
        # TODO: Change load image calls.
        self.pyxda.loadimage.dirpath = self.panel.dirPath
        #self.pyxda.loadimage.dirpath = '/Users/Mike/GSAS-II/Exercises/images/'
        #self.pyxda.jobqueue.put(['processexist'])
        return

    @on_trait_change('panel.left_arrow', post_init=True)
    def _left_arrow_fired(self):
        #TODO: Define Left Arrow
        self.pyxda.jobqueue.put(['updatecache', ['left']])
        return
    
    @on_trait_change('panel.right_arrow', post_init=True)
    def _right_arrow_fired(self):
        #TODO: Define Right Arrow
        self.pyxda.jobqueue.put(['updatecache', ['right']])
        return


    def updateImageContainer(self):
            
        container = GridContainer(bgcolor="lightgrey", shape=(1,1), 
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
