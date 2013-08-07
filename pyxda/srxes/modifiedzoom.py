from chaco.tools.api import BetterSelectingZoom


class ModifiedZoomTool(BetterSelectingZoom):

    def __init__(self, component=None, *args, **kw):
        BetterSelectingZoom.__init__(self, component, *args, **kw)
        self.ratiohistory = [self.component.aspect_ratio]
        return

    
    def selecting_left_up(self, event):
        '''Changes aspect ratio of plot to match ROI.'''
        x1, y1 = self._screen_start
        x2, y2 = event.x, event.y
        if (y2 - y1) == 0:
            x2 = x1
            y2 = y1
        else:
            plotwidth = self.component.width
            plotheight = self.component.height
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            drawn_aspect = width / height
            #self.component.aspect_ratio = drawn_aspect
            if drawn_aspect > 1.0:
                self.component.height = plotheight/drawn_aspect
                self.component.x = 0
                self.component.y = (plotheight - plotheight/drawn_aspect) / 2
            else:
                self.component.width = plotwidth*drawn_aspect
                self.component.y = 0
                self.component.x = (plotwidth - plotwidth/drawn_aspect) / 2

            self.ratiohistory.append(drawn_aspect)

        if self.drag_button in ("left", None):
            self._end_select(event)

    def _next_state_pressed(self):
        """ Called when the tool needs to advance to the next state in the
        stack.

        The **_history_index** will have already been set to the index
        corresponding to the next state.
        """

        self._current_state().apply(self)
        drawn_aspect = self.ratiohistory[self._history_index]
        if drawn_aspect > 1.0:
            self.component.height = 500/drawn_aspect
        else:
            self.component.width = 500*drawn_aspect

    def _prev_state_pressed(self):
        """ Called when the tool needs to advance to the previous state in the
        stack.

        The **_history_index** will have already been set to the index
        corresponding to the previous state.
        """
        self._history[self._history_index+1].revert(self)
        drawn_aspect = self.ratiohistory[self._history_index]
        if drawn_aspect > 1.0:
            self.component.height = 500/drawn_aspect
        else:
            self.component.width = 500*drawn_aspect

    def _reset_state_pressed(self):
        """ Called when the tool needs to reset its history.

        The history index will have already been set to 0.
        """
        for state in self._history[::-1]:
            state.revert(self)
        self._history = []
        #self.component.aspect_ratio = self.ratiohistory[0]
        self.ratiohistory = [self.component.aspect_ratio ]
        
