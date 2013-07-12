#!/usr/bin/env python

from traits.api import HasTraits, Directory, Button, Int
from enthought.traits.ui.api import View,Item, Group, HGroup, HSplit
from chaco.api import GridContainer

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    dirpath = Directory()
    left_arrow = Button('<')
    right_arrow = Button('>')
    reset = Button('Reset')
    quality = Button('Generate Intensity Map')
    dirpath = Directory()

    group = Group(
                Item('dirpath', show_label = False),
                HGroup(
                    Item('left_arrow', label = "Image"), 
                    Item('right_arrow', show_label = False)),
                Item('quality', show_label = False),
                show_border = True,
                padding = 10
                )
    
    view = View(group)

