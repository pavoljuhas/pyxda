#!/usr/bin/env python

from traits.api import HasTraits, Directory, Button, Int, Str
from enthought.traits.ui.api import View, Item, Group, HGroup, HSplit
from chaco.api import GridContainer

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    dirpath = Directory()
    left_arrow = Button('<')
    right_arrow = Button('>')
    reset = Button('Reset')
    quality = Button('Generate Intensity Map')
    dirpath = Directory()
    spacer = Str('              ')
    index = Int(0)
    of = Str('of')
    datalistlength = Int(0) 

    group = Group(
                Item('dirpath', show_label = False),
                HGroup(
                    HGroup(
                        Item('left_arrow', show_label = False), 
                        Item('right_arrow', show_label = False),
                        padding = 5
                          ),
                    Item('spacer', show_label = False, style = 'readonly'),
                    HGroup(
                        Item('index', show_label = False, width=-30, height=-20),
                        Item('of', show_label = False, style = 'readonly'),
                        Item('datalistlength', show_label = False, style = 'readonly'),
                        padding = 5
                          ) 
                      ),
                Item('quality', show_label = False),
                show_border = True,
                )
    
    view = View(group)

