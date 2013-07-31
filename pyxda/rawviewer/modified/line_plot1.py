#!/usr/bin/env python
# coding=utf-8
##############################################################################
#
# pyxda.srxes       X-ray Data Analysis Library
#                   (c) 2013 National Synchrotron Light Source II,
#                   Brookhaven National Laboratory, Upton, NY.
#                   All rights reserved.
#
# File coded by:    Mark Lange
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

# Major library imports
import sys
from numpy import linspace
from scipy.special import jn

# Enthought library imports
from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance, Event
from traitsui.api import Item, Group, View

# Chaco imports
from chaco.api import ArrayPlotData, HPlotContainer, Plot
from chaco.tools.api import PanTool
from betterselectingzoom import BetterSelectingZoom

#===============================================================================
# Attributes to use for the plot view.
size=(500,500)
title="Basic x-y plots"

#===============================================================================
# # Demo class that is used by the demo.py application.
#===============================================================================
class Demo(HasTraits):
    
    def __init__(self, **kwargs):
        super(Demo, self).__init__()
        self.add_trait('zoom', BetterSelectingZoom)
    
    plot = Instance(Component)
    
    traits_view = View(
                    Group(
                        Item('plot', editor=ComponentEditor(),
                             show_label=False, resizable = True),
                        orientation = "vertical"),
                    resizable=False, title=title,
                    width = size[0], height = size[1]
                    )

    def _plot_default(self):
         return self._create_plot_component()
        
    #===============================================================================
    # # Create the Chaco plot.
    #===============================================================================
    def _create_plot_component(self):
        
        selected = Event()
    
        # Create some x-y data series to plot
        x = linspace(-2.0, 10.0, 100)
        pd = ArrayPlotData(index = x)
        for i in range(5):
            pd.set_data("y" + str(i), jn(i,x))
    
        # Create some line plots of some of the data
        plot1 = Plot(pd, title="Line Plot", padding=50, border_visible=True)
        plot1.legend.visible = True
        plot1.plot(("index", "y0", "y1", "y2"), name="j_n, n<3", color="red")
    
        # Attach some tools to the plot
        plot1.tools.append(PanTool(plot1))
        
        self.zoom = BetterSelectingZoom(component=plot1, tool_mode="box", always_on=False, selection_completed = selected)
        plot1.overlays.append(self.zoom)

        container = HPlotContainer()
        container.add(plot1)
        
        self.zoom.on_trait_change(self.selection_changed, 'ratio')
    
        return container
    
    #This function is called when the left mouse button raises and 
    #completes the zoom selection. 
    def selection_changed(self):
        ratio = self.plot.plot_components[0].overlays[2].ratio
        print ratio
        sys.stdout.flush()
        
        if ratio == 1.0:
            self.plot.aspect_ratio = None
            self.plot.height = 500
            self.plot.width = 500
            self.plot.x = 0
            self.plot.y = 0
        elif ratio > 1.0:
            self.plot.width = 500
            self.plot.height = 500/ratio
            self.plot.x = 0
            self.plot.y = 250 - 0.5*self.plot.height
        else:
            self.plot.height = 500
            self.plot.width = 500*ratio
            self.plot.y = 0
            self.plot.x = 250 - 0.5*self.plot.width     
        
        return

demo = Demo()

if __name__ == "__main__":
    demo.configure_traits()
    

#--EOF---
