#!/usr/bin/env python

from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.menu import NoButtons
from enthought.traits.ui.api import View, Item, UItem, HSplit, VGroup, Group
from traits.api import on_trait_change
from enable.api import ComponentEditor,Component
from chaco.api import GridContainer
import sys
import pyxda as px
from handler import PyXDAHandler

class UserInterface(HasTraits):
    
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
    view = View(HSplit(Group(UItem('imagecontainer', editor=ComponentEditor(),
                            dock='vertical'), 
                            show_border = True),
                       VGroup(
                            Item('panel', style="custom"),
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
    @on_trait_change('panel.image_select.arrow_keys.left_arrow', post_init=True)
    def _left_arrow_fired(self):
        self.pyxda.jobqueue.put(['updatecache', ['left']])
        self.panel.index = self.pyxda.imagecache.imagepos
        self.panel.text  = ' of '+str(self.pyxda.datalistlength)
        return
    
    @on_trait_change('panel.image_select.arrow_keys.right_arrow', post_init=True)
    def _right_arrow_fired(self):
        self.pyxda.jobqueue.put(['updatecache', ['right']])
        self.panel.index = self.pyxda.imagecache.imagepos
        self.panel.text  = ' of '+str(self.pyxda.datalistlength)
        return
    
    @on_trait_change('panel.quality', post_init=True)
    def _quality_fired(self):
        self.pyxda.jobqueue.put(['createcmap'])
        return
    
    @on_trait_change('panel.dirpath', post_init=True)
    def _dirpath_changed(self):
        #print 'startload request sent'
        self.pyxda.jobqueue.put(['startload', [self.panel.dirpath]])
        self.panel.image_select.index_display.index = self.pyxda.imagecache.imagepos
        self.panel.image_select.index_display.text  = ' of '+str(self.pyxda.datalistlength)
        return
    
    @on_trait_change('panel.scale', post_init=True)
    def _scale_changed(self):
        #Siwtches between linear and log scale  
        #TODO: Add functionality     
        if self.panel.scale == 'linear':
            print 'linear!'
        else:
            print 'logorithmic'
    
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
