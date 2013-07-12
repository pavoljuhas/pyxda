#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from chaco.tools.api import PanTool, ZoomTool, LineInspector
from chaco.api import ArrayPlotData, Plot, jet, BaseTool
from enable.api import BaseTool, KeySpec, ColorTrait, KeySpec
from traits.api import Any, HasTraits, Instance, Tuple, Int, Event


class ImageIndexTool(BaseTool):

    callback = Any()
    arrow_cb = Any()
    token  = Any()
    left_key = KeySpec("Left",)
    right_key = KeySpec("Right",)

    def normal_left_down(self, event):
        self._update_plots(event)

    def _update_plots(self, event):
        plot = self.component
        ndx = plot.map_index((event.x, event.y),
                                 threshold=5.0, index_only=True)
        if ndx and ndx[0] >= 0 and ndx[1] >= 0:
            self.callback(self, ndx)
            #print ndx

    def normal_key_pressed(self, event):
        if self.left_key.match(event):
            print 'Left Arrow'
            self.arrow_cb(self, -1)
        elif self.right_key.match(event):
            print 'Right Arrow'
            self.arrow_cb(self, 1)

class Display(HasTraits, object):

    def __init__(self, **kwargs):
        super(Display, self).__init__()
        ndx = -1, -1
        self.add_trait('ndx', Tuple(ndx))
        self.add_trait('left', Event)
        self.add_trait('right', Event)
    
    def _index_callback(self, tool, ndx):
        print 'Pixel clicked: (%d, %d)' % ndx
        self.ndx = ndx 

    def _arrow_callback(self, tool, n):
        if n == 1:
            self.right = {}
        else:
            self.left = {}

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
        zoom = ZoomTool(component=plot, tool_mode="box", always_on=False,
                            color='transparent', aspect_ratio=1.0,
                            zoom_factor=1.25, pointer='sizing',
                            prev_state_key=KeySpec('n'),
                            next_state_key=KeySpec('m')
                            )
        plot.overlays.append(zoom)
        plot.zoom = zoom
        '''
        xcursor = LineInspector(plot, axis="index_x", color="white",
            inspect_mode="indexed", write_metadata=True, is_listener=False)
        ycursor = LineInspector(plot, axis="index_y", color="white",
            inspect_mode="indexed", write_metadata=True, is_listener=False)
        plot.overlays.append(xcursor)
        plot.overlays.append(ycursor)
        '''
        if title == 'Total Intensity Map':
            plot.tools.append(ImageIndexTool(plot, callback=self._index_callback,
                                             arrow_cb=self._arrow_callback))
        return
