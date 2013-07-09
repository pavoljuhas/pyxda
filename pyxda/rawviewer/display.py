from chaco.tools.api import PanTool, ZoomTool, LineInspector
from chaco.api import ArrayPlotData, Plot, jet, BaseTool
from enable.api import BaseTool, KeySpec




# Major library imports
from numpy import linspace, meshgrid, pi
from scipy.special import jn

# Enthought library imports
from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Item, Group, View

# Chaco imports
from chaco.api import ArrayPlotData, ColorBar, HPlotContainer, jet, \
                                 LinearMapper, Plot
from chaco.tools.api import PanTool, RangeSelection, \
                                       RangeSelectionOverlay, ZoomTool
                                       
                                       
                                       


class ImageIndexTool(BaseTool):
        
    def normal_left_down(self, event):
        self._update_plots(event)

    def _update_plots(self, event):
        plot = self.component
        ndx = plot.map_index((event.x, event.y),
                                 threshold=5.0, index_only=True)
        print ndx

class Display(object):

    def plot2DImage(self, data, plot=None, title=None):
        rv = self.plotImage(data, title, plot)
        return rv

    def plotImage(self, image, title, plot):
        '''plot one image
        image:     2d ndarray or ssp matrix
        title:     string, plot title
        plot:      plot instance to be update, if None, a plot instance will be created

        return:    plot instance'''
        if plot == None:
            pd = ArrayPlotData()
            pd.set_data('imagedata', image)
            plot = Plot(pd, default_origin = "bottom left")
            imgPlot = plot.img_plot("imagedata", colormap=jet, name='image')[0]
            self._appendTools(imgPlot)
            plot.title = title
            plot.bgcolor = 'white'
            
            # Create the colorbar, handing in the appropriate range and colormap
            colormap = plot.color_mapper
            colorbar = ColorBar(index_mapper=LinearMapper(range=colormap.range),
                        color_mapper=colormap,
                        plot=plot,
                        orientation='v',
                        resizable='v',
                        width=30,
                        padding=20)
            colorbar.padding_top = plot.padding_top
            colorbar.padding_bottom = plot.padding_bottom
            
        else:
            plot.data.set_data('imagedata', image)
            plot.title = title
        plot.aspect_ratio = float(image.shape[1]) / image.shape[0]
        plot.invalidate_draw()
        return plot

    def _appendTools(self, plot):
        '''append xy position, zoom, pan tools to plot
        '''
        plot.tools.append(PanTool(plot))
        zoom = ZoomTool(component=plot, tool_mode="box", always_on=False)
        plot.overlays.append(zoom)
        plot.zoom = zoom
        xcursor = LineInspector(plot, axis="index_x", color="white",
            inspect_mode="indexed", write_metadata=True, is_listener=False)
        ycursor = LineInspector(plot, axis="index_y", color="white",
            inspect_mode="indexed", write_metadata=True, is_listener=False)
        plot.overlays.append(xcursor)
        plot.overlays.append(ycursor)
        plot.tools.append(ImageIndexTool(plot))

        return


    
    class ImageIndexTool(BaseTool):
        
        def normal_left_down(self, event):
            self._update_plots(event)

        def _update_plots(self, event):
            plot = self.component
            ndx = plot.map_index((event.x, event.y),
                                 threshold=5.0, index_only=True)
            print ndx
