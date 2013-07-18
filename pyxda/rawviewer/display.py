#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from chaco.tools.api import PanTool, ZoomTool, LineInspector, ScatterInspector
from chaco.api import ArrayPlotData, Plot, jet, BaseTool, add_default_axes, \
                        add_default_grids, ScatterInspectorOverlay

from enable.api import BaseTool, KeySpec, ColorTrait, KeySpec
from traits.api import Any, HasTraits, Instance, Tuple, Int, Event, Float, Property, \
                cached_property

import numpy as np


####################

SIZE = 12

####################

class KBInputTool(BaseTool):
    
    arrow_cb = Any()
    left_key = KeySpec("Left",)
    right_key = KeySpec("Right",)

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
        ndx = -1
        self.add_trait('ndx', Int())
        self.add_trait('left', Event)
        self.add_trait('right', Event)
    
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
            if not title == 'Total Intensity Map':
                plot.x_axis.visible = False
                plot.y_axis.visible = False
                imgPlot = plot.img_plot("imagedata", colormap=jet, name='image')[0]
            # TODO: mess with color maps on else block    
            else:
                imgPlot = plot.img_plot("imagedata", colormap=jet, name='image')[0]
                self._appendCMapTools(imgPlot)

            self._appendTools(imgPlot, title)
        else:
            plot.data.set_data('imagedata', image)
            plot.title = title
        plot.aspect_ratio = float(image.shape[1]) / image.shape[0]
        plot.invalidate_draw()
        return plot

    def plotRRMap(self, rr, title, plot=None):
        if plot == None:
            pd = ArrayPlotData(y=np.array([0]), x=np.array([0]))
            plot = Plot(pd)
            self._setData(rr, title, plot)
            plot.plot(('x', 'y'), name=title, type="scatter", color='green',
                      marker="circle", marker_size=6)
            self._appendCMapTools(plot, title)
            plot.title = title
            plot.bgcolor = 'white'
            left, bottom = add_default_axes(plot)
            hgrid, vgrid = add_default_grids(plot)
        else:
            self._setData(rr, title, plot)
        plot.request_redraw()
        return plot

    def _setData(self, rr, title, plot):
        if rr == None:
            return
        ydata = plot.data.get_data('y')
        if len(ydata) == 1 and ydata[0] == 0:
            ydata = np.array([rr])
        else:
            ydata = np.append(ydata, [rr])
            plot.data.set_data('x', range(len(ydata)))
        plot.data.set_data('y', ydata)
        #print rr
        #print plot.data.get_data('y')
        #print plot.data.get_data('x')
        return

    def _appendTools(self, plot, title):
        '''append xy position, zoom, pan tools to plot
        '''
        plot.tools.append(PanTool(plot))
        zoom = ZoomTool(component=plot, tool_mode="box", always_on=False,
                            color='transparent', aspect_ratio=1.0,
                            zoom_factor=1.25, pointer='sizing',
                            prev_state_key=KeySpec('n'),
                            next_state_key=KeySpec('m'),
                            x_min_zoom_factor = 1.0,
                            y_min_zoom_factor = 1.0
                            )
        plot.overlays.append(zoom)
        plot.zoom = zoom
        plot.tools.append(KBInputTool(plot, arrow_cb=self._arrow_callback))
        return

    def _appendCMapTools(self, plot, title):
        my_plot = plot.plots[title][0]
        self.index_datasource = my_plot.index
        self.index_datasource.on_trait_change(self._metadata_handler,
                                              "metadata_changed")
        my_plot.tools.append(ScatterInspector(my_plot, selection_mode="toggle",
                                          persistent_hover=False))

        my_plot.overlays.append(ScatterInspectorOverlay(my_plot,
                                hover_color = "transparent",
                                hover_marker_size = 10,
                                hover_outline_color = "purple",
                                hover_line_width = 2,
                                selection_marker_size = 8,
                                selection_color = "lawngreen")
                               )
        zoom = ZoomTool(component=plot, tool_mode='box', always_on=False, 
                            zoom_factor=1.25, color='transparent')
        plot.overlays.append(zoom)
        plot.tools.append(PanTool(plot))
        return

    def _metadata_handler(self):
        sel_indices = self.index_datasource.metadata.get('selections', [])
        hover_indices = self.index_datasource.metadata.get('hover', [])
        print "Selection indices:", sel_indices
        print "Hover indices:", hover_indices
        if sel_indices: 
            self.ndx = sel_indices[-1]
        return
        

