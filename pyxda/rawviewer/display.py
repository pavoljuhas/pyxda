from chaco.tools.api import PanTool, ZoomTool
from image import Image
from chaco.api import ArrayPlotData, Plot, jet
from enable.api import BaseTool, KeySpec


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
        else:
            plot.data.set_data('imagedata', image)
            plot.title = title
        plot.aspect_ratio = float(image.shape[1]) / image.shape[0]
        plot.invalidate_draw()
        return plot

    def _appendTools(self, plot):
        '''append xy position, zoom, pan tools to plot
        '''
        # TODO: Add ROI tool.
        plot.tools.append(PanTool(plot))
        zoom = ZoomTool(component=plot, tool_mode="box", always_on=False)
        plot.overlays.append(zoom)
        plot.zoom = zoom
        return
