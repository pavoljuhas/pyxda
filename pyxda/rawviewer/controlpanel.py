#!/usr/bin/env python

from enthought.traits.api import HasTraits, Directory, Button, Int
from enthought.traits.ui.api import View,Item, Group, HGroup, HSplit

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    dirpath = Directory()
    left_arrow = Button('<')
    right_arrow = Button('>')
    reset = Button('Reset')
    quality = Button('Total Intensity')

    view = View(
                Group(
                    Item('dirpath', label = "Load"),
                    HGroup(
                        Item('left_arrow', label = "Image"), 
                        Item('right_arrow', show_label = False)),
                   Item('quality', show_label = False),
                   show_border = True,
                   padding = 10
                   )
               )
