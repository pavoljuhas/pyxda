#!/usr/bin/env python

from traits.api import HasTraits, Instance, Directory
from enthought.traits.ui.api import View,Item, Group, HSplit, Handler, VSplit, \
                    HGroup, VGroup
from traits.api import *
from enable.api import ComponentEditor,Component, KeySpec
from enthought.traits.ui.menu import NoButtons
from chaco.api import ArrayPlotData, Plot, jet, GridContainer

from rawviewer import RawViewer
from controlpanel import ControlPanel
from display import Display
from handler import PyXDAHandler
import sys

class UserInterface(HasTraits):

    def __init__(self, **kwargs):
        super(UserInterface, self).__init__()
        self.add_trait('rawviewer', RawViewer())
        self.add_trait('panel', self.rawviewer.panel)
        self.add_trait('display', self.rawviewer.display)
        self.add_trait('cmap', self.rawviewer.cmap)
        self.rawviewer.startProcessJob()

        self.display.on_trait_change(self._left_arrow_fired, 'left')
        self.display.on_trait_change(self._right_arrow_fired, 'right')
        self.panel.sync_trait('datalistlength', self.rawviewer)
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
                title = 'Raw Viewer')

    #############################
    # UI Action Handling
    #############################
    @on_trait_change('panel.left_arrow', post_init=True)
    def _left_arrow_fired(self):
        self.rawviewer.jobqueue.put(['updatecache', ['left']])
        return
    
    @on_trait_change('panel.right_arrow', post_init=True)
    def _right_arrow_fired(self):
        self.rawviewer.jobqueue.put(['updatecache', ['right']])
        return
    
    @on_trait_change('panel.quality', post_init=True)
    def _quality_fired(self):
        self.rawviewer.jobqueue.put(['createcmap'])
        return
    
    @on_trait_change('panel.dirpath', post_init=True)
    def _dirpath_changed(self):
        self.rawviewer.jobqueue.put(['startload', [self.panel.dirpath]])
    
    def _ndx_changed(self):
        self.rawviewer.jobqueue.put(['changendx'])
    @on_trait_change('rawviewer.imagecache.imagepos', post_init=True)
    def _imagepos_changed(self):
        self.panel.index = self.rawviewer.imagecache.imagepos + 1 
        
    def updateImageContainer(self):
            
        container = GridContainer(bgcolor="transparent", shape=(1,1), 
                                    use_backbuffer=True)
        self.imagecontainer = container

        cont = getattr(self.rawviewer, 'imageplot')
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
