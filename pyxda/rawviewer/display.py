#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from chaco.tools.api import PanTool, ZoomTool, LineInspector
from chaco.api import ArrayPlotData, Plot, jet, BaseTool
from enable.api import BaseTool, KeySpec, ColorTrait, KeySpec
from traits.api import Any, HasTraits, Instance, Tuple, Int, Event, Float, Property, \
                cached_property


####################

SIZE = 12

####################

class ImageIndexTool(LineInspector):

    callback = Any()
    dl = Int()

    current_index = Tuple(0, 1)
    current_position = Property(depends_on=['current_index'])

    def normal_mouse_move(self, event):
        return

    def normal_mouse_leave(self, event):
        return

    def normal_left_down(self, event):
        print 'Click pixel' 
        self._get_pixel_position(event)
        return

    def _current_index_changed(self):
        print 'Index Changed'
        self.component.request_redraw()
        return

    @cached_property
    def _get_current_position(self):
        print 'calculate position'
        plot = self.component
        ndx, ndy = self.current_index
        xdata, ydata = plot.index.get_data()
        x = xdata.get_data()[ndx]
        y = ydata.get_data()[ndy]
        print x,y
        return x,y

    def _set_current_position(self, traitname, args):
        print 'set current position'
        plot = self.component
        xds, yds = plot.index.get_data()
        ndx = xds.reverse_map(args[0])
        ndy = yds.reverse_map(args[1])
        if ndx is not None and ndy is not None:
            self.current_index = ndx, ndy

    def _get_pixel_position(self, event):
        print 'get pixel position'
        plot = self.component
        ndx= plot.map_index((event.x, event.y),
                                 threshold=5.0, index_only=True)
        if ndx and ndx[0] >= 0 and ndx[1] >= 0:
            self.current_index = ndx
            plot.request_redraw()
            self.callback(self, ndx)
            event.handled = True
            
            print ndx
        return

    def draw(self, gc, view_bounds=None):
        """ Draws a vertical line through screen point (sx,sy) having the height
        of the tool's component.
        """
        print 'draw'
        plot = self.component
        if plot is None:
            return
        sx, sy = plot.map_screen([self.current_position])[0]
        print sx
        if sx is not None and sy is not None:
            dl = plot.x2 / SIZE
            print 'plot.x2 = %d' % plot.x2
            print 'dl = %d' % dl
            self._draw_box(gc, sx, sy, dl)
        return


    def _draw_box(self, gc, sx, sy, dl):
        plot = self.component
        if sx < plot.x or sx > plot.x2 or sy < plot.y or sy > plot.y2:
            return
        print 'draw box'
        with gc:
            gc.set_stroke_color(self.color_)
            gc.set_line_width(self.line_width)
            gc.set_line_dash(self.line_style_)
            gc.move_to(sx, sy)
            gc.line_to(sx, sy+dl)
            gc.move_to (sx+dl, sy)
            gc.line_to(sx+dl, sy+dl)
            gc.move_to (sx, sy)
            gc.line_to(sx+dl, sy)
            gc.move_to (sx, sy+dl)
            gc.line_to(sx+dl, sy+dl)
            
            print 'x = %d\ny = %d' % (sx, sy)
            print 'x2 = %d\ny2 = %d' % (sx, sy+dl)
            gc.stroke_path()
        return

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
        print plot
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
        '''
        xcursor = LineInspector(plot, axis="index_x", color="white",
            inspect_mode="indexed", write_metadata=True, is_listener=False)
        ycursor = LineInspector(plot, axis="index_y", color="white",
            inspect_mode="indexed", write_metadata=True, is_listener=False)
        plot.overlays.append(xcursor)
        plot.overlays.append(ycursor)
        '''

        #if title == 'Total Intensity Map':
            #plot.overlays.append(ImageIndexTool(plot, callback=self._index_callback))
        return

    def appendCMapTools(self, plot, ndx):
        index = (ndx%SIZE, ndx/SIZE+SIZE-1)
        imgPlot = plot.plots.values()[0]
        plot.overlays.append(ImageIndexTool(imgPlot, callback=self._index_callback,
                                                current_index=index))
        return

