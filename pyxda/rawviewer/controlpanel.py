#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enthought.traits.api import HasTraits, Directory, Button, Str, Int
from enthought.traits.ui.api import View,Item, Group, HGroup, HSplit, HFlow
from enthought.traits.ui.api \
    import View, ArrayEditor, Item
import sys

class IndexDisplay(HasTraits):
    
    def __init__(self, **kwargs):
        self.add_trait('index', Int(0))
        self.add_trait('text', Str(' of 0'))

    view = View(
               HGroup(
                    Item('index', show_label = False),
                    Item('text', show_label = False)
               )
            )
            
class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    def __init__(self, **kwargs):
        self.add_trait('index_display', IndexDisplay)
    
    dirpath = Directory()
    reset = Button('Reset')
    quality = Button('Generate Intensity Map')
    left_arrow = Button('<')
    right_arrow = Button('>')
    dirpath = Directory()
    
    index = Int(0)
    text = Str(' of 0')
    
    view = View(
                Item('dirpath', show_label = False),
                HGroup(
                    Item('left_arrow', show_label = False),
                    Item('right_arrow', show_label = False),
                    #This is my first attempt, Notice the extra space.
                    Group(Item('index', show_label= False, width = -20), show_border = True),
                    Group(Item('text', show_label=False, style = 'readonly'), show_border = True),
                    show_border = True
                ),
                #This is my second attempt. This seemed to work for 'panel' in userinterface. What am I doing wrong? 
                Item('index_display', style = "readonly", width = -30),
                Item('quality', show_label = False),
                width = 0.25
                )
                         
def main():
    ui = ControlPanel()
    ui.configure_traits()

if __name__ == '__main__':
    sys.exit(main())

    

