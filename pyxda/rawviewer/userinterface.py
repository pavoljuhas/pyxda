#!/usr/bin/env python

from enthought.traits.api import HasTraits, Instance, Directory
from display import Display
from enthought.traits.ui.api import View,Item, Group, HSplit, Handler, VSplit, \
                    HGroup, VGroup
from traits.api import *
from enable.api import ComponentEditor,Component
from enthought.traits.ui.menu import NoButtons
from enthought.traits.ui.key_bindings import KeyBinding, KeyBindings
from chaco.api import ArrayPlotData, Plot, jet, GridContainer

import pyxda as px
from controlpanel import ControlPanel
from handler import PyXDAHandler
import sys

class UserInterface(HasTraits):
    '''    
    left = KeyBinding(binding1='Z', binding2='z', method_name='left')
    right = KeyBinding(binding1='X', binding2='x', method_name='_right_arrow_fired')
    bindings = KeyBindings(left, right) 
    '''
    def __init__(self, **kwargs):
        super(UserInterface, self).__init__()
        self.add_trait('pyxda', px.PyXDA())
        self.add_trait('panel', self.pyxda.panel)
        self.add_trait('display', self.pyxda.display)
        self.add_trait('cmap', self.pyxda.cmap)
        self.pyxda.startProcessJob()
        #self.pyxda.loadimage.start()

        self.display.on_trait_change(self._ndx_changed, 'ndx')
        self.imagecontainer = Instance(Component)
        self.updateImageContainer()

    # TODO: Adjust view
    view = View(HSplit(Item('imagecontainer', editor=ComponentEditor(),
                            dock='vertical'),
                       VGroup(
                            Item('panel', style="custom", padding=10),
                            Item('cmap', editor=ComponentEditor()),
                            show_labels = False
                             ),
                       show_labels=False,
                      ),
                resizable=True,
                height=0.75, width=0.75,
                handler=PyXDAHandler(),
                buttons=NoButtons,
                #key_bindings=bindings,
                title = 'Raw Viewer')

    #############################
    # UI Action Handling
    #############################
    @on_trait_change('panel.left_arrow', post_init=True)
    def _left_arrow_fired(self):
        self.pyxda.jobqueue.put(['updatecache', ['left']])
        return
    
    @on_trait_change('panel.right_arrow', post_init=True)
    def _right_arrow_fired(self):
        self.pyxda.jobqueue.put(['updatecache', ['right']])
        return
    
    @on_trait_change('panel.quality', post_init=True)
    def _quality_fired(self):
        self.pyxda.jobqueue.put(['createcmap'])
        return
    
    @on_trait_change('panel.dirpath', post_init=True)
    def _dirpath_changed(self):
        #print 'startload request sent'
        self.pyxda.jobqueue.put(['startload', [self.panel.dirpath]])
    
    def _ndx_changed(self):
        self.pyxda.jobqueue.put(['changendx'])

    def updateImageContainer(self):
            
        container = GridContainer(bgcolor="transparent", shape=(1,1), 
                                    use_backbuffer=True)
        self.imagecontainer = container

        cont = getattr(self.pyxda, 'imageplot')
        if cont in container._components:
            container.remove(cont)
        
        container.add(cont)
        
        container.get_preferred_size()
        container.invalidate_draw()
        return

def main():
    ui = UserInterface()
    ui.configure_traits()

if __name__ == '__main__':
    sys.exit(main())
