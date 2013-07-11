# -*- coding: utf-8 -*-
from enthought.traits.api import HasTraits, Instance, Directory
from display import Display
from enthought.traits.ui.api import View,Item, Group, HSplit, Handler, VSplit, \
                    HGroup, VGroup
from traits.api import *
from enable.api import ComponentEditor,Component
from enthought.traits.ui.menu import NoButtons
from chaco.api import ArrayPlotData, Plot, jet, GridContainer

import pyxda as px

from enthought.chaco.color_bar import ColorBar
from enthought.etsconfig.api import ETSConfig
from enthought.traits.api import HasTraits, Float, Button, RGBColor
from enthought.traits.ui.api import View, Controller
from enthought.traits.ui.key_bindings import KeyBinding, KeyBindings




maximize = KeyBinding(binding1='M', binding2='m',
        method_name='toggle_maximized')
fullscreen = KeyBinding(binding1='F', binding2='f',
        method_name='toggle_fullscreen')
bindings = KeyBindings(maximize, fullscreen)


class PyXDAUI(HasTraits):
    
    def __init__(self, **kwargs):
        super(PyXDAUI, self).__init__()
        self.add_trait('pyxda', px.PyXDA())
        self.add_trait('panel', self.pyxda.panel)
        self.add_trait('display', self.pyxda.display)
        self.add_trait('cmap', self.pyxda.cmap)
        self.pyxda.startProcessJob()
        self.pyxda.loadimage.start()

        self.panel.sync_trait('dirpath', self.pyxda.loadimage, mutual=False)
        self.add_trait('dirpath', Directory())
        #self.pyxda.jobqueue.put(['processexist'])
        self.imagecontainer = Instance(Component)
        self.updateImageContainer()

    # TODO: Adjust view    
    view = View(HSplit(Item('imagecontainer', editor=ComponentEditor(),
                            dock='vertical'),
                       VGroup(
                            Item('panel', style="custom", show_label = False),
                            Item('cmap', editor=ComponentEditor(), show_label = False)),
                       show_labels=False,
                      ),
                resizable=True,
                height=0.75, width=0.75,
                key_bindings=bindings,
                buttons=NoButtons
                )
                
    def toggle_maximized(self, info):
        if ETSConfig.toolkit == 'wx':
            current_mode = info.ui.control.IsMaximized()
            info.ui.control.Maximize(not current_mode)
        else:
            if info.ui.control.isMaximized():
                info.ui.control.showNormal()
            else:
                info.ui.control.showMaximized()
 
    def toggle_fullscreen(self, info):
        if ETSConfig.toolkit == 'wx':
            current_mode = info.ui.control.IsFullScreen()
            info.ui.control.ShowFullScreen(not current_mode)
        else:
            if info.ui.control.isFullScreen():
                info.ui.control.showNormal()
            else:
                info.ui.control.showFullScreen()

    #############################
    # UI Action Handling
    #############################
    
    @on_trait_change('dirpath', post_init=True)
    def _load_data_fired(self):
        '''Loads data for display.'''
        # TODO: Change load image calls.
        #self.pyxda.loadimage.dirpath = dirpath
        #'/Users/Mike/Downloads/1208NSLSX17A_LiRh2O4/'
        #self.pyxda.loadimage.dirpath = '/Users/Mike/GSAS-II/Exercises/images/'
        return

    @on_trait_change('panel.left_arrow', post_init=True)
    def _left_arrow_fired(self):
        self.pyxda.jobqueue.put(['updatecache', ['left']])
        return
    
    def toggle_left(self):
        self.pyxda.jobqueue.put(['updatecache', ['left']])
        return
    
    @on_trait_change('panel.right_arrow', post_init=True)
    def _right_arrow_fired(self):
        self.pyxda.jobqueue.put(['updatecache', ['right']])
        return
    
    def toggle_right(self):
        self.pyxda.jobqueue.put(['updatecache', ['right']])
        return
    
    # Properly define.
    @on_trait_change('panel.quality', post_init=True)
    def _quality_fired(self):
        self.pyxda.jobqueue.put(['createcmap'])
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
