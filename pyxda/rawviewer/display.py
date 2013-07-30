#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from chaco.tools.api import PanTool, ZoomTool, LineInspector, ScatterInspector, \
                            RangeSelection, RangeSelectionOverlay, BroadcasterTool, \
                            LineSegmentTool

from chaco.api import ArrayPlotData, Plot, jet, BaseTool, add_default_axes, \
                        add_default_grids, ScatterInspectorOverlay, BarPlot, \
                        LinearMapper, ColorBar, ToolbarPlot

from enable.api import BaseTool, KeySpec, ColorTrait, KeySpec
from traits.api import Any, HasTraits, Instance, Tuple, Int, Event, Float, Property, \
                cached_property, Str

import numpy as np
from modifiedzoom import ModifiedZoomTool


####################
# TODO: globalize size
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

class MyLineDrawer(LineSegmentTool):
    """
    This class demonstrates how to customize the behavior of the
    LineSegmentTool via subclassing.
    """

    def _finalize_selection(self):
        print "Dataspace points:"
        for point in self.points:
            print "\t", point

class Display(HasTraits, object):

    def __init__(self, queue, **kwargs):
        super(Display, self).__init__()
        self.jobqueue = queue
        self.add_trait('filename', Int())
    
    def _arrow_callback(self, tool, n):
        if n == 1:
            self.jobqueue.put(['updatecache', ['right']])
        else:
            self.jobqueue.put(['updatecache', ['left']])

    def _metadata_handler(self):
        sel_indices = self.index_datasource.metadata.get('selections', [])
        hover_indices = self.index_datasource.metadata.get('hover', [])
        print "Selection indices:", sel_indices
        print "Hover indices:", hover_indices
        if sel_indices:
            self.jobqueue.put(['changendx', [sel_indices[-1]]])
            print sel_indices[-1]
        if hover_indices:
            self.filename = hover_indices[0]
            print 'self.filename', self.filename
        else:
            self.filename = -1
        return

    def plotImage(self, image, plot=None):
        '''plot one image
        image:     Image object
        plot:      plot instance to be update, if None, a plot instance will be created
        return:    plot instance'''
        if plot == None:
            pd = ArrayPlotData()
            pd.set_data('imagedata', image.data)
            plot = Plot(pd, default_origin = "bottom left", padding=0)
            #plot.title = image.name
            plot.bgcolor = 'white'
            plot.fixed_preferred_size = (100, 100)
            plot.x_axis.visible = False
            plot.y_axis.visible = False
            self.imageplot = plot

            # TODO: mess with color maps on else block    
            imgPlot = plot.img_plot("imagedata", colormap=jet, name='image')[0]
            self.imgPlot = imgPlot
            self._appendImageTools(imgPlot)
            #plot.overlays.append(MyLineDrawer(plot))
        else:
            plot.data.set_data('imagedata', image.data)
            imgPlot = plot.plots['image'][0]
            #plot.title = image.name
        plot.aspect_ratio = float(image.data.shape[1]) / image.data.shape[0]
        plot.invalidate_draw()
        return plot

    def plotRRMap(self, rr, rrchoice, plot=None):
        if plot == None:
            pd = ArrayPlotData(y=np.array([0]), x=np.array([0]))
            plot = Plot(pd, padding=(70, 5, 0, 0))
            self._setData(rr, plot)
            plot.plot(('x', 'y'), name='rrplot', type="scatter", color='green',
                      marker="circle", marker_size=6)
            #plot.title = 'rrplot'
            plot.value_axis.title = rrchoice
            #plot.y_axis.visible = False
            plot.bgcolor = 'white'
            plot.aspect_ratio = 2.5
            plot.fixed_preferred_size = (100, 50)
            #left, bottom = add_default_axes(plot)
            hgrid, vgrid = add_default_grids(plot)
            self._appendCMapTools(plot)
        else:
            self._setData(rr, plot)
        plot.request_redraw()
        return plot

    def _setData(self, rr, plot):
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

    def plotHistogram(self, image, plot=None):
        if plot == None:
            pd = ArrayPlotData(y=np.array([0]), x=np.array([0]))
            plot = Plot(pd, padding=(70, 10, 0, 0))
            plot.plot(('x', 'y'), name='Histogram', type='bar', bar_width=5.0, color='auto')
            #plot.title = 'Histogram'
            plot.line_color = 'black'
            plot.bgcolor = "white"
            plot.fixed_preferred_size = (100, 30)
            plot.value_range.low = 0
            add_default_grids(plot)
            plot.value_axis.title = "Histogram"
            self._appendHistogramTools(plot)
            '''
            plot.overlays.append(PlotAxis(plot, orientation='left'))
            plot.overlays.append(PlotAxis(plot, orientation='bottom'))
            '''
        else:
            data = np.histogram(image.data, bins=10000)
            index = np.delete(data[1], data[1].size-1)
            values = data[0]

            plot.data.set_data('x', index)
            plot.data.set_data('y', values)
        plot.request_redraw()
        return plot


    def _appendImageTools(self, plot):
        '''append xy position, zoom, pan tools to plot
        '''
        plot.tools.append(PanTool(plot))
        
        zoom = ZoomTool(component=plot, tool_mode="box", always_on=False,
                            color='transparent',
                            zoom_factor=1.25, pointer='sizing',
                            prev_state_key=KeySpec('n'),
                            next_state_key=KeySpec('m'),
                            x_min_zoom_factor = 1.0,
                            y_min_zoom_factor = 1.0
                            )
        plot.overlays.append(zoom)
        plot.zoom = zoom
        plot.tools.append(KBInputTool(plot, arrow_cb=self._arrow_callback))
        #plot.overlays.append(MyLineDrawer(plot))

        colormap = plot.color_mapper
        colorbar = ColorBar(index_mapper=LinearMapper(range=colormap.range),
                        color_mapper=colormap,
                        plot=plot,
                        orientation='v',
                        resizable='v',
                        width=30,
                        padding=20)

        range_selection = RangeSelection(component=colorbar)
        colorbar.tools.append(range_selection)
        rangeselect = RangeSelectionOverlay(component=colorbar,
                                                   border_color="white",
                                                   alpha=0.8,
                                                   fill_color="lightgray")
        colorbar.overlays.append(rangeselect)
        range_selection.listeners.append(plot)
        self.colorbar = colorbar
        return
    
    def _appendHistogramTools(self, plot):
        plot.tools.append(PanTool(plot))
        zoom = ZoomTool(component=plot, tool_mode="box", always_on=False,
                            color='transparent',
                            zoom_factor=1.25, pointer='sizing',
                            enter_zoom_key=KeySpec('p'),
                            prev_state_key=KeySpec('n'),
                            next_state_key=KeySpec('m'),
                            x_min_zoom_factor = 1.0,
                            y_min_zoom_factor = 1.0
                            )
        plot.overlays.append(zoom)
        plot.zoom = zoom
        
        my_plot = plot.plots["Histogram"][0]

        selected = Event()
        self.range_selection = RangeSelection(component=my_plot, selection_completed = selected)
        self.range_selection.on_trait_change(self._selection_changed, 'selection_completed')

        my_plot.tools.append(self.range_selection)

        rangeselect = RangeSelectionOverlay(component=my_plot,
                                                   border_color="white",
                                                   alpha=0.8,
                                                   fill_color="lightgray")
        my_plot.overlays.append(rangeselect)
        self.range_selection.listeners.append(self.imgPlot)
        return

    def _selection_changed(self):
        print 'Region highlighted'
        print self.range_selection._selection
        return


    def _appendCMapTools(self, plot):
        my_plot = plot.plots['rrplot'][0]
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


        

