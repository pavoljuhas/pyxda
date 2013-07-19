# -*- coding: utf-8 -*-
# Major library imports
import sys 
import numpy as np
import fabio

# Enthought library imports
from enable.api import ComponentEditor, Component
from traits.api import HasTraits, Instance, Event
from traitsui.api import View, UItem

# Chaco imports
from chaco.tools.api import PanTool
from chaco.tools.api import RangeSelection, RangeSelectionOverlay
from chaco.api import ArrayDataSource, BarPlot, DataRange1D, \
                         LinearMapper, add_default_grids, PlotAxis, \
                         VPlotContainer, PlotLabel

#TODO. Add On_Highlight - DO SOMETHING
#      Remove required initialize data variable
class Histogram(HasTraits):
    '''Histogram class for displaying image intesity distribution.'''
    
    bar_plot = Instance(Component)
    
    traits_view = View(
                      UItem('bar_plot', editor=ComponentEditor()),
                      width = 0.75, height = 0.75
                  )
            
    def plot(self, data):
        data = data.ravel()
        histData = np.histogram(data, bins = 100000)
        index = histData[1]
        self.index = np.delete(index, index.size-1)
        self.values = histData[0]
        self.configure_traits()
        
                
    def _bar_plot_default(self):

        # Default data
        idx = self.index
        vals = self.values
        selected = Event()

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
        
        #Range Selection
        self.rangeselect = RangeSelection(plot, selection_completed = selected)
        plot.active_tool = self.rangeselect
        plot.overlays.append(RangeSelectionOverlay(component=plot))
        
        #Fires method upon highlighting
        selection = plot.active_tool
        selection.on_trait_change(self._selection_changed, 'selection_completed')
        
        #Container for the plot
        container = VPlotContainer(spacing = 20, padding = 50)               
        container.add(plot)
        container.overlays.append(PlotLabel("Histogram", component=container, font="Arial 30"))
        
        return container
    
    def _selection_changed(self):
        print 'Region highlighted'
        sys.stdout.flush()
        return
        
        
#For testing
if __name__ == "__main__":
    image = fabio.open('//BNLNT1C/Users/M/mlange/pyXDA-Development/1208NSLSX17A_LiRh2O4/LiRh2O4_w2k_080K-00006.tif')
    data = image.data
    
    demo = Histogram()
    demo.plot(data)
