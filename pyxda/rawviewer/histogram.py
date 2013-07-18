# -*- coding: utf-8 -*-
# Major library imports
import numpy as np
import fabio

# Enthought library imports
from enable.api import ComponentEditor, Component
from traits.api import HasTraits, Instance
from traitsui.api import View, UItem

# Chaco imports
from chaco.tools.api import PanTool
from chaco.tools.simple_zoom import SimpleZoom
from chaco.api import ArrayDataSource, BarPlot, DataRange1D, \
                         LinearMapper, add_default_grids, PlotAxis, \
                         VPlotContainer, PlotLabel

#TODO. Add On_Highlight - DO SOMETHING
#      Remove required initialize data variable
class Histogram(HasTraits):
    '''
    Histogram class for displaying image intesity distribution.
    
    Takes in image data on instatiation. Creates view that displays a histogram
    of intensity distrubution.
    
    Left mouse pans the image.
    Right mouse highlights a region.
    Mouse scroll zooms in and out.
    '''
    
    bar_plot = Instance(Component)
    
    traits_view = View(
                      UItem('bar_plot', editor=ComponentEditor()),
                      width = 0.75, height = 0.75
                  )

    def __init__(self, data, **kw):
        super(Histogram, self).__init__(**kw)
        
        data = data.ravel()
        histData = np.histogram(data, bins = 100000)
        index = histData[1]
        self.index = np.delete(index, index.size-1)
        self.values = histData[0]
                
    def _bar_plot_default(self):

        # Default data
        idx = self.index
        vals = self.values

        # Mappers
        index = ArrayDataSource(idx)
        index_range = DataRange1D(index, low = -5000, high = 75000)
        index_mapper = LinearMapper(range=index_range)

        value = ArrayDataSource(vals)
        value_range = DataRange1D(value, high = 7000)
        value_mapper = LinearMapper(range=value_range)

        # The bar plot
        plot = BarPlot(index = index, value = value,
                             index_mapper = index_mapper,
                             value_mapper = value_mapper,
                             line_color = 'black',
                             bgcolor = "white",
                             border_visible = True)
                             
        #Plot overlays                     
        add_default_grids(plot)
        plot.overlays.append(PlotAxis(plot, orientation='left'))
        plot.overlays.append(PlotAxis(plot, orientation='bottom'))
        plot.tools.append(PanTool(plot, constrain=True,
                                        constrain_direction="x"))
        plot.overlays.append(SimpleZoom(plot, drag_button="right",
                                            always_on=True,
                                            tool_mode="range",
                                            axis="index"))
    
    
        container = VPlotContainer(spacing = 20, padding = 50)               
        container.add(plot)
        container.overlays.append(PlotLabel("Histogram", component=container, font="Arial 30"))
        return container
        
        
#For testing
if __name__ == "__main__":
    image = fabio.open('//BNLNT1C/Users/M/mlange/pyXDA-Development/1208NSLSX17A_LiRh2O4/LiRh2O4_w2k_080K-00006.tif')
    data = image.data
    demo = Histogram(data)
    demo.configure_traits()
