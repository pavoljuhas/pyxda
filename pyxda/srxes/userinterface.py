#!/usr/bin/env python
# coding=utf-8
##############################################################################
#
# pyxda.srxes       X-ray Data Analysis Library
#                   (c) 2013 National Synchrotron Light Source II,
#                   Brookhaven National Laboratory, Upton, NY.
#                   All rights reserved.
#
# File coded by:    Michael Saltzman
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

from traits.api import *
from traitsui.api import View, Item, Group, HSplit, VSplit, VGroup, UItem
from enable.api import ComponentEditor, Component
from chaco.api import GridContainer, HPlotContainer, VPlotContainer
from chaco import default_colormaps
from pyface.api import ImageResource

from controlpanel import ControlPanel, MetadataPanel
from processcenter import ProcessCenter
from display import Display

import sys
import time
import os

ICON = ImageResource('logo.ico', search_path=[os.path.dirname(__file__)])

class UserInterface(HasTraits):
    '''A user interface that handles interactions with the images/data.
    
    |  control -- JobControl object that handles the internal functionality
    |  cpanel -- contains tools to interact with the data, shown in upper right
    |  mdpanel -- contains the metadata for the image, shown in lower left
    |  imagepanel -- contains all of the image related plots, shown on left
    |  rrpanel -- contains the RR plots that have been created, shown on right
    '''

    def __init__(self, **kwargs):
        super(UserInterface, self).__init__()
        self.add_trait('process', ProcessCenter())
        self.add_trait('cpanel', ControlPanel())
        self.add_trait('mdpanel', MetadataPanel())

        self.process.startProcessJob()
        self.cpanel.sync_trait('datalistlength', self.process)
        self.cpanel.sync_trait('message', self.process)

        self.imagepanel = Instance(Component)
        self.createImagePanel()
        self.rrpanel = Instance(Component)
        self.rrpanel = VPlotContainer(stack_order = 'top_to_bottom',
                                        resizeable='', use_backbuffer=True,
                                        bgcolor='transparent')
        self.rrpanel.get_preferred_size()
        return

    view = View(
             HSplit(
               VSplit(
                    UItem('imagepanel', editor=ComponentEditor(), 
                                            padding=0, height=0.825),
                    UItem('mdpanel', style="custom", height=127, width=700,
                                            resizable=True),
                     ),
               VGroup(
                    UItem('cpanel', style="custom", width=-430, padding=10),
                    UItem('rrpanel', editor=ComponentEditor(), style='custom')
                     ),
                show_labels=False,
                  ),
            resizable = True,
            height = 0.95, width = 1.0,
            title = 'SrXes',
            icon = ICON
            )

    #############################
    # UI Action Handling
    #############################
    @on_trait_change('cpanel.left_arrow', post_init=True)
    def _left_arrow_fired(self):
        '''Left arrow/key pressed. Sends request to load previous image.'''
        self.process.jobqueue.put(['updatecache', ['left']])
        return
    
    @on_trait_change('cpanel.right_arrow', post_init=True)
    def _right_arrow_fired(self):
        '''Right arrow/key pressed. Sends request to load next image.'''
        self.process.jobqueue.put(['updatecache', ['right']])
        return
    
    @on_trait_change('cpanel.generate', post_init=True)
    def _generate_fired(self):
        '''Generate pressed. Sends request to create specified RR plot.'''
        self.process.jobqueue.put(['plotrr', [self.cpanel.rrchoice]])
        time.sleep(0.5)
        self.updateRRPanel(self.cpanel.rrchoice)
        return
    
    @on_trait_change('cpanel.dirpath', post_init=True)
    def _dirpath_changed(self):
        '''A directory has been chosen. Sends request to start load thread.'''
        self.process.jobqueue.put(['startload', [self.cpanel.dirpath]])
        return
    
    @on_trait_change('process.pic', post_init=True)
    def _pic_changed(self):
        '''Updates the index and metadata when the current image changes.'''
        pic =  self.process.pic
        self.cpanel.index = pic.n + 1
        self.mdpanel.name = pic.name
        if pic.metadata:
            for key in pic.metadata.keys():
                setattr(self.mdpanel, key, pic.metadata[key])
        else:
            for key in self.mdpanel.editable_traits():
                if key != 'name':
                    setattr(self.mdpanel, key, '')
        return

    @on_trait_change('process.display.filenum', post_init=True)
    def _filenum_changed(self):
        '''Handles interactions with the RR plots. When a point is hovered
        over, its filename is displayed in the control panel.
        '''
        #print 'filenum changed'
        n = self.process.display.filenum
        if n == -1:
            self.cpanel.message = ''
        else:
            name = self.process.datalist[n].name
            self.cpanel.message = '%d: %s' % (n+1, name)
        return

    @on_trait_change('cpanel.colormap', post_init=True)
    def _colormap_changed(self):
        '''A new colormap has been selected. Sends request to update cmap.'''
        self.process.jobqueue.put(['updatecmap', [self.cpanel.colormap]])
        return

    def createImagePanel(self):
        '''Creates the image panel and fills it with the associated plots. 
        The plots included are the image plot, histogram, and 1D plot. Data
        can be set for these plots without changing the Plot objects.
        '''
        cont = VPlotContainer(stack_order = 'top_to_bottom',
                                bgcolor = 'transparent',
                                use_backbuffer=True)

        imageplot = getattr(self.process, 'imageplot')
        colorbar = getattr(self.process.display, 'colorbar')
        histogram = getattr(self.process, 'histogram')
        plot1d = getattr(self.process, 'plot1d')

        imgcont = HPlotContainer(imageplot, colorbar, bgcolor = 'transparent',
                                    spacing = 20.0)
        cont.add(imgcont)
        cont.add(histogram)
        cont.add(plot1d)
        
        self.imagepanel = cont
        self.imagepanel.get_preferred_size()
        self.imagepanel.invalidate_draw()
        return
    
    def updateRRPanel(self, choice):
        '''Fills the rrpanel with new RR plots.

        choice -- the name of the RR to check for
        '''
        rrplots = getattr(self.process, 'rrplots')
        
        try:
            if rrplots[choice] not in self.rrpanel._components:
                self.rrpanel.add(rrplots[choice])
        except KeyError: 
            return

        if len(self.rrpanel._components) > 3:
            self.rrpanel.remove(self.rrpanel._components[0])

        self.rrpanel.invalidate_and_redraw()
        return

def main():
    ui = UserInterface()
    ui.configure_traits()

if __name__ == '__main__':
    sys.exit(main())
