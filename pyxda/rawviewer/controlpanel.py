from enthought.traits.api import HasTraits, Instance, Directory
from enthought.traits.ui.api import View,Item, Group, HSplit, Handler, VSplit, \
                    HGroup, VGroup
from traits.api import *
from enthought.traits.api import HasTraits, Float, Button, RGBColor, Property, Bool

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    #Traits for this class
    dirpath = Directory('')
    left_arrow = Button('<')
    right_arrow = Button('>')
    reset = Button('Reset')
    quality = Button('Quality Assessment')
    
    #GUI for this panel
    view = View(
               Group(
                   Item('dirpath', label = "Folder Path"),
                   HGroup(
                       Item('left_arrow', label = "Image"), 
                       Item('right_arrow', show_label = False),
                       Item('reset', show_label = False),
                   ),
                   Item('quality', show_label = False),
                   show_border = True,
                   label = 'Controls'
               )
           )

ControlPanel.configure_traits