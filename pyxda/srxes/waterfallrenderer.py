"""
This plot displays the audio spectrum from the microphone.

Based on updating_plot.py
"""
# Major library imports
import pyaudio
from numpy import zeros, linspace, short, fromstring, transpose, array
from scipy import fft

# Enthought library imports
from enable.api import Window, Component, ComponentEditor
from traits.api import HasTraits, Instance, List, Range
from traitsui.api import Item, Group, View, Handler
from pyface.timer.api import Timer

# Chaco imports
from chaco.api import (Plot, ArrayPlotData, HPlotContainer, VPlotContainer,
    AbstractMapper, LinePlot, LinearMapper, DataRange1D, ArrayDataSource)

import filereader as fr

NUM_SAMPLES = 418
SAMPLING_RATE = 11025
SPECTROGRAM_LENGTH = 50

class WaterfallRenderer(LinePlot):

    # numpy arrays of the same length
    values = List(args=[])

    # Maps each array in values into a contrained, short screen space
    x2_mapper = Instance(AbstractMapper)
    y2_mapper = Instance(AbstractMapper)

    _cached_data_pts = List()
    _cached_screen_pts = List()

    def _gather_points(self):
        if not self._cache_valid:
            if not self.index or len(self.values) == 0:
                return

            index = self.index.get_data()
            values = self.values

            numindex = len(index)
            if numindex == 0 or all(len(v)==0 for v in values) or all(numindex != len(v) for v in values):
                self._cached_data_pts = []
                self._cache_valid = True

            self._cached_data_pts = [transpose(array((index, v))) for v in values]
            self._cache_value = True
        return

    def get_screen_points(self):
        self._gather_points()
        return [self.map_screen(pts, i, i) for i, pts in enumerate(self._cached_data_pts)]

    def map_screen(self, data_array, y_offset=None, x_offset=None):
        """ data_offset, if provided, is a float that will be mapped
        into screen space using self.value_mapper and then added to
        mapping data_array with y2_mapper.  If data_offset is not
        provided, then y2_mapper is used.
        """
        if len(data_array) == 0:
            return []
        x_ary, y_ary = transpose(data_array)
        if y_offset is not None:
            dy = self.value_mapper.map_screen(y_offset)
            sy = self.y2_mapper.map_screen(y_ary) + dy
        else:
            sy = self.value_mapper.map_screen(y_ary)

        if x_offset is not None:
            dx = self.index_mapper.map_screen(x_offset)
            sx = self.x2_mapper.map_screen(x_ary) + dx
        else:
            sx = self.self.index_mapper.map_screen(x_ary)

        if self.orientation == "h":
            return transpose(array((sx, sy)))
        else:
            return transpose(array((sy, sx)))

#============================================================================
# Create the Chaco plot.
#============================================================================

def _create_plot_component(obj):
    # Spectrogram plot
    
    obj.data = fr.getDataSets('.chi')
    frequencies = obj.data[0][0]
    index = ArrayDataSource(data=frequencies)

    values = [obj.data[i][1] for i in xrange(len(obj.data))]
    print len(obj.data[1][1])
    print len(obj.data)
    p = WaterfallRenderer(index = index, values = values,
            index_mapper = LinearMapper(range = DataRange1D(low=0, high=SPECTROGRAM_LENGTH)),
            value_mapper = LinearMapper(range = DataRange1D(low=0, high=SPECTROGRAM_LENGTH)),
            x2_mapper = LinearMapper(low_pos=0, high_pos=100,
                            range=DataRange1D(low=10.0, high=101.0)),
            y2_mapper = LinearMapper(low_pos=0, high_pos=100,
                            range=DataRange1D(low=0, high=600000))
            )
    spectrogram_plot = p
    obj.spectrogram_plot = p
    dummy = Plot()
    dummy.padding = 50
    dummy.index_axis.mapper.range = p.index_mapper.range
    dummy.index_axis.title = "Frequency (hz)"
    dummy.add(p)

    c2 = VPlotContainer()
    c2.add(dummy)

    return c2


def get_audio_data():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLING_RATE,
                     input=True, frames_per_buffer=NUM_SAMPLES)
    audio_data  = fromstring(stream.read(NUM_SAMPLES), dtype=short)
    stream.close()
    normalized_data = audio_data / 32768.0
    return (abs(fft(normalized_data))[:NUM_SAMPLES/2], normalized_data)


# HasTraits class that supplies the callable for the timer event.
class TimerController(HasTraits):

    def onTimer(self, *args):
        '''
        spectrum, time = get_audio_data()
        spec_data = self.spectrogram_plot.values[1:] + [spectrum]
        print spectrum
        self.spectrogram_plot.values = spec_data
        self.spectrogram_plot.request_redraw()
        '''
        return

#============================================================================
# Attributes to use for the plot view.
size = (900,700)
title = "Audio Spectrum Waterfall"

#============================================================================
# Demo class that is used by the demo.py application.
#============================================================================

class DemoHandler(Handler):

    def closed(self, info, is_ok):
        """ Handles a dialog-based user interface being closed by the user.
        Overridden here to stop the timer once the window is destroyed.
        """

        info.object.timer.Stop()
        return

class Demo(HasTraits):

    plot = Instance(Component)

    controller = Instance(TimerController, ())

    timer = Instance(Timer)

    xoffset = Range(0.0, 100.0)
    yoffset = Range(0.0, 100.0)

    traits_view = View(
                    Group(
                        Item('plot', editor=ComponentEditor(size=size),
                             show_label=False),
                        Item('xoffset', label='X Offset'),
                        Item('yoffset', label='Y Offset'), 
                        orientation = "vertical"),
                    resizable=True, title=title,
                    width=size[0]+75, height=size[1]+75,
                    handler=DemoHandler
                    )

    def __init__(self, **traits):
        super(Demo, self).__init__(**traits)
        self.plot = _create_plot_component(self.controller)
                    
        self.on_trait_change(self.changeXOffset, 'xoffset')
        self.on_trait_change(self.changeYOffset, 'yoffset')

    def changeXOffset(self):
        self.controller.spectrogram_plot.index_mapper.range.high = self.xoffset
        self.controller.spectrogram_plot.request_redraw
        return

    def changeYOffset(self):
        self.controller.spectrogram_plot.value_mapper.range.high = self.yoffset
        self.controller.spectrogram_plot.request_redraw
        return

    def edit_traits(self, *args, **kws):
        # Start up the timer! We should do this only when the demo actually
        # starts and not when the demo object is created.
        self.timer = Timer(10, self.controller.onTimer)
        return super(Demo, self).edit_traits(*args, **kws)

    def configure_traits(self, *args, **kws):
        # Start up the timer! We should do this only when the demo actually
        # starts and not when the demo object is created.
        self.timer = Timer(10, self.controller.onTimer)
        return super(Demo, self).configure_traits(*args, **kws)


popup = Demo()

if __name__ == "__main__":
    popup.configure_traits()
