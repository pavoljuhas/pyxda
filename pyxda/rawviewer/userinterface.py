#!/usr/bin/env python

<<<<<<< HEAD
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
    
=======
from traits.api import HasTraits, Instance, Directory
from enthought.traits.ui.api import View,Item, Group, HSplit, Handler, VSplit, \
                    HGroup, VGroup, InstanceEditor, UItem
from traits.api import *
from enable.api import ComponentEditor,Component, KeySpec
from enthought.traits.ui.menu import NoButtons
from chaco.api import ArrayPlotData, Plot, jet, GridContainer, HPlotContainer, \
                        VPlotContainer

from rawviewer import RawViewer
from controlpanel import ControlPanel, MetadataPanel
from display import Display
from handler import PyXDAHandler
import sys
import time

class UserInterface(HasTraits):

>>>>>>> b7bad4b0fa82c7a6a603d3078f3cbcec0cc45e9a
    def __init__(self, **kwargs):
        super(UserInterface, self).__init__()
        self.add_trait('rawviewer', RawViewer())
        self.add_trait('cpanel', ControlPanel())
        self.add_trait('mdpanel', MetadataPanel())

        self.rawviewer.startProcessJob()
        self.cpanel.sync_trait('datalistlength', self.rawviewer)

        self.imagepanel = Instance(Component)
        self.createImagePanel()
        self.rrpanel = Instance(Component)
        self.rrpanel = VPlotContainer(stack_order = 'top_to_bottom',
                                        resizeable='', use_backbuffer=True,
                                        bgcolor='transparent')
        self.rrpanel.get_preferred_size()

    # TODO: Adjust view
<<<<<<< HEAD
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
=======
    view = View(
             HSplit(
               VSplit(
                    UItem('imagepanel', editor=ComponentEditor(), padding=0),
                    UItem('mdpanel', style="custom", padding=5, height=85, width=700),
                     ),
               VGroup(
                    UItem('cpanel', style="custom", width=-430, padding=10),
                    UItem('rrpanel', editor=ComponentEditor(), style='custom')
                     ),
                show_labels=False,
                  ),
            resizable = True,
            height = 0.96, width = 1.0,
            handler = PyXDAHandler(),
            buttons = NoButtons,
            title = 'Raw Viewer')
>>>>>>> b7bad4b0fa82c7a6a603d3078f3cbcec0cc45e9a

    #############################
    # UI Action Handling
    #############################
<<<<<<< HEAD
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
=======
    @on_trait_change('cpanel.left_arrow', post_init=True)
    def _left_arrow_fired(self):
        self.rawviewer.jobqueue.put(['updatecache', ['left']])
        return
    
    @on_trait_change('cpanel.right_arrow', post_init=True)
    def _right_arrow_fired(self):
        self.rawviewer.jobqueue.put(['updatecache', ['right']])
>>>>>>> b7bad4b0fa82c7a6a603d3078f3cbcec0cc45e9a
        return
    
    @on_trait_change('cpanel.generate', post_init=True)
    def _generate_fired(self):
        self.rawviewer.jobqueue.put(['plotrr', [self.cpanel.rrchoice]])
        time.sleep(0.5)
        self.updateRRPanel(self.cpanel.rrchoice)
        return
    
    @on_trait_change('cpanel.dirpath', post_init=True)
    def _dirpath_changed(self):
<<<<<<< HEAD
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
=======
        self.rawviewer.jobqueue.put(['startload', [self.cpanel.dirpath]])
    
    @on_trait_change('rawviewer.pic', post_init=True)
    def _pic_changed(self):
        pic =  self.rawviewer.pic
        self.cpanel.index = pic.n + 1
        self.mdpanel.name = pic.name
        if pic.metadata:
            for key in pic.metadata.keys():
                setattr(self.mdpanel, key, pic.metadata[key])
        return
    @on_trait_change('rawviewer.display.filename', post_init=True)
    def _filename_changed(self):
        print 'filename changed'
        if self.rawviewer.display.filename == -1:
            self.cpanel.filename = ''
        else:
            self.cpanel.filename = self.rawviewer.datalist[self.rawviewer.display.filename].name

>>>>>>> b7bad4b0fa82c7a6a603d3078f3cbcec0cc45e9a
    
    # TODO: Update
    def createImagePanel(self):
        cont = VPlotContainer(stack_order = 'top_to_bottom',
                                bgcolor = 'transparent',
                                use_backbuffer=True)

        imageplot = getattr(self.rawviewer, 'imageplot')
        colorbar = getattr(self.rawviewer.display, 'colorbar')
        histogram = getattr(self.rawviewer, 'histogram')
        plot1d = getattr(self.rawviewer, 'plot1d')

        imgcont = HPlotContainer(imageplot, colorbar, bgcolor = 'transparent',
                                    spacing = 20.0)
        cont.add(imgcont)
        cont.add(histogram)
        cont.add(plot1d)

        
<<<<<<< HEAD
        container.add(cont)
        container.get_preferred_size()
        container.invalidate_draw()
=======
        self.imagepanel = cont
        self.imagepanel.get_preferred_size()
        self.imagepanel.invalidate_draw()
        return

    def updateRRPanel(self, choice):
        rrplots = getattr(self.rawviewer, 'rrplots')
        
        if rrplots[choice] not in self.rrpanel._components:
            self.rrpanel.add(rrplots[choice])

        self.rrpanel.invalidate_and_redraw()
>>>>>>> b7bad4b0fa82c7a6a603d3078f3cbcec0cc45e9a
        return

def main():
    ui = UserInterface()
    ui.configure_traits()

if __name__ == '__main__':
    sys.exit(main())
