#!/usr/bin/env python

from chaco.tools.api import PanTool, ZoomTool, LineInspector
from chaco.api import ArrayPlotData, Plot, jet, BaseTool
from traits.api import Any, HasTraits, Tuple
                                
class ImageIndexTool(BaseTool):

    callback = Any()
    token  = Any()
        
    def normal_left_down(self, event):
        self._update_plots(event)

    def _update_plots(self, event):
        plot = self.component
        ndx = plot.map_index((event.x, event.y),
                                 threshold=5.0, index_only=True)
        if ndx and ndx[0] >= 0 and ndx[1] >= 0:
            self.callback(self, ndx)
            #print ndx

class Display(HasTraits, object):

    def __init__(self, **kwargs):
        super(Display, self).__init__()
        ndx = -1, -1
        self.add_trait('ndx', Tuple(ndx))
    
    def _index_callback(self, tool, ndx):
        self.ndx = ndx 
        #print 'Display'
        #print self.ndx

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
            plot.title = title
            plot.bgcolor = 'white'
            if not title == 'Total Intensity':
                plot.x_axis.visible = False
                plot.y_axis.visible = False
                imgPlot = plot.img_plot("imagedata", colormap=jet, name='image')[0]
            # TODO: mess with color maps on else block    
            else:
                imgPlot = plot.img_plot("imagedata", colormap=jet, name='image')[0]

            self._appendTools(imgPlot, title)
        else:
            plot.data.set_data('imagedata', image)
            plot.title = title
        plot.aspect_ratio = float(image.shape[1]) / image.shape[0]
        plot.invalidate_draw()
        return plot

    def _appendTools(self, plot, title):
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
        if title == 'Total Intensity Map':
            plot.tools.append(ImageIndexTool(plot, callback=self._index_callback))
        return
