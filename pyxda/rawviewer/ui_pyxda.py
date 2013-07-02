from loadimages import getTiffImages
from enthought.traits.api import HasTraits, Instance, Directory
from display import Display
from enthought.traits.ui.api import View,Item, Group, HGroup, HSplit, VSplit, Handler
from traits.api import *

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    #Traits for this class
    display = Display()
    dirPath = Directory()
    load_data = Button('LOAD')
    left_arrow = Button('<')
    right_arrow = Button('>')
    numViewers = Enum('One View', 'Nine Views')
    message = Str()

    index = 0 #Used to keep track of images
    
    #GUI for this panel
    view = View(
               Group(
                   HGroup(
                       Item('dirPath', label = "Folder Path"),
                       Item('load_data', show_label=False)
                   ),
                   HGroup(
                       Item('left_arrow', label = "Image"), 
                       Item('right_arrow', show_label = False),
                   ),
                   Item('numViewers', label = "Views"),
                   show_border = True,
                   label = 'Controls'
               )
           )
    
    #Actions to be executed on events
    def _load_data_fired(self):
        '''Loads data for display.'''
        # TODO: Needs to be updated for scaleability.
        self.pyxda.plotDirectory(self.dirPath)
        
    def _left_arrow_fired(self):
        '''Changes index being displayed backwards''' 
        if self.index>0:
            self.index = self.index-1
            self.pyxda.updatePlot(self.index)
            
        return
            
    def _right_arrow_fired(self):
        '''Changes index being displayed forwards'''
        if self.index<9:
            self.index = self.index+1
            self.pyxda.updatePlot(self.index)
            
        return
        
if __name__ == '__main__':
    panel = ControlPanel(display=Display(), test = 14)
    panel.configure_traits()
