# Major library imports
import numpy
import fabio

# Enthought library imports
from enable.api import ComponentEditor, Component
from traits.api import HasTraits, Instance, Array
from traitsui.api import UItem, View

# Chaco imports
from chaco.api import Plot, ArrayPlotData, LassoOverlay, add_default_axes, add_default_grids
from chaco.tools.api import PanTool, ZoomTool, DragZoom, RangeSelection, RangeSelectionOverlay

class Histogram(HasTraits):
    plot = Instance(Component)
    traits_view = View(UItem('plot', editor=ComponentEditor()),
                       width=0.5, height=0.5, resizable=True, 
                      )

    def __init__(self, data, **kw):
        super(Histogram, self).__init__(**kw)
        
        data = data.ravel()
        histData = numpy.histogram(data, bins = 5000)
        index = histData[1]
        self.index = numpy.delete(index, index.size-1)
        self.values = histData[0]
                
    def _plot_default(self):
        
        #Create Plot
        plot_data = ArrayPlotData(index=self.index)
        plot_data.set_data('values', self.values)
        plot = Plot(plot_data)
        plot.plot(('index', 'values'), type='bar', bar_width=0.8, color='black')
        
        '''# The PanTool allows panning around the plot
        self.plot.tools.append(PanTool(self.plot))

        # The ZoomTool tool is stateful and allows drawing a zoom
        # box to select a zoom region.
        zoom = ZoomTool(self.plot, tool_mode="box", always_on=False)
        self.plot.overlays.append(zoom)'''
        
        #Range Selection Tool
        '''plot.active_tool = RangeSelection(plot, left_button_selects = True)
        plot.overlays.append(RangeSelectionOverlay(component=plot))
        plot.bgcolor = "white"
        plot.padding = 50'''
        
        return plot
        
        

if __name__ == "__main__":
    image = fabio.open('//BNLNT1C/Users/M/mlange/pyXDA-Development/1208NSLSX17A_LiRh2O4/LiRh2O4_w2k_080K-00006.tif')
    data = image.data
    demo = Histogram(data)
    demo.configure_traits()
