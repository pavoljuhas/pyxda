from loadimages import getTiffImages
from enthought.traits.api import HasTraits, Instance, Directory
from display import Display
from enthought.traits.ui.api import View,Item, Group, HSplit, VSplit, Handler
from traits.api import *

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    display = Display()
    dirPath = Directory()
    load_data = Button('LOAD')
    left_arrow = Button('<')
    right_arrow = Button('>')
    message = Str()
    
    index = 0

    view = View(
               Group(
                   HSplit(
                       Item('left_arrow', label = "Prev/Next"), 
                       Item('right_arrow', show_label = False),
                    ),
                    HSplit(
                        Item('dirPath'),
                        Item('load_data', show_label=False),
                    )
               )
           )

    def _load_data_fired(self):
        '''Loads data for display.'''
        # TODO: Needs to be updated for scaleability.
        self.pyxda.initDisplay(self.dirPath)
        
    def _left_arrow_fired(self):
        if self.index>0:
            self.index = self.index-1
            self.pyxda.updatePlot(self.index)
            
        return
            
    def _right_arrow_fired(self):
        if self.index<9:
            self.index = self.index+1
            self.pyxda.updatePlot(self.index)
            
        return
        
if __name__ == '__main__':
    panel = ControlPanel(camera=Camera(), display=Display(), test = 14)
    panel.configure_traits()
