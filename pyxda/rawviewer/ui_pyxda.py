from loadimages import getTiffImages
from enthought.traits.api import HasTraits, Instance, Directory
from display import Display
from enthought.traits.ui.api import View,Item, Group, HGroup, HSplit, VSplit, Handler
from traits.api import *
from enthought.traits.ui.key_bindings \
    import KeyBinding, KeyBindings

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    #Traits for this class
    display = Display()
    dirPath = Directory()
    left_arrow = Button('<')
    right_arrow = Button('>')
    reset = Button('Reset')
    quality = Button('Quality Assessment')
    message = Str('One')

    index = 0 #Used to keep track of images
    
    #GUI for this panel
    view = View(
               Group(
                   Item('dirPath', label = "Folder Path"),
                   Item('message'),
                   HGroup(
                       Item('left_arrow', label = "Image"), 
                       Item('right_arrow', show_label = False),
                       Item('reset', show_label = False)
                   ),
                   Item('quality', show_label = False),
                   show_border = True,
                   label = 'Controls'
               )
           )
    
    #Actions to be executed on events
    @on_trait_change('dirPath')
    def _load_data(self):
        '''Loads data for display.'''
        # TODO: Needs to be updated for scaleability.
        try:
            self.pyxda.plotDirectory(self.dirPath)
        except:
            pass
        
    def _left_arrow_fired(self):
        '''Changes index being displayed backwards''' 
        try:
            if self.index>0:
                self.index = self.index-1
                self.pyxda.updatePlot(self.index)
        except:
            pass
            
        return
            
    def _right_arrow_fired(self):
        '''Changes index being displayed forwards'''
        try:
            if self.index<9:
                self.index = self.index+1
                self.pyxda.updatePlot(self.index)
        except:
             pass  
                  
        return
                       
if __name__ == '__main__':
    panel = ControlPanel(display=Display(), test = 14)
    panel.configure_traits()
