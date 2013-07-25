#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enthought.traits.api import HasTraits, Instance, Directory, Button, Str, Int, Enum
from enthought.traits.ui.api import View,Item, HGroup, Group
import sys

class IndexDisplay( HasTraits ):
    index  = Int(0)
    text   = Str(' of 0')
    
    view = View( HGroup(Item('index', show_label = False), 
                               Item('text', show_label = False, style = 'readonly')
                              )
                  )

class ArrowKeys(HasTraits):
    left_arrow = Button('<')
    right_arrow = Button('>')

    view = View(
               HGroup(
                   Item('left_arrow', show_label = False),
                   Item('right_arrow', show_label = False),
                   padding = 0
               )
           )

class ImageSelect(HasTraits):
    index_display = Instance(IndexDisplay)
    arrow_keys = Instance(ArrowKeys)
    
    def __init__(self, **kwargs):
        self.index_display = IndexDisplay()
        self.arrow_keys = ArrowKeys()
    
    view = View(
               HGroup(
                    Item('index_display', style = 'custom', label = 'Image', width = -55),
                    Item('arrow_keys', style = 'custom', show_label = False)
               )
           )

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    dirpath = Directory()
    reset = Button('Reset')
    quality = Button('Generate Intensity Map')
    Reduced = Enum('linear', 'log')
    dirpath = Directory()
    
    image_select = Instance(ImageSelect)
    
    def __init__(self, **kwargs):
        self.image_select = ImageSelect()
        
    view = View(
               Group(
                   Item('dirpath', show_label = False),
                   HGroup(
                       Group(Item('image_select', style = 'custom', show_label = False, width = -300), show_border = True),
                       Item('quality', show_label = False),
                   ),
               show_border = True
               ),
               width = 0.40
            )
                         
if __name__ == '__main__':
    ui = ControlPanel()
    ui.configure_traits()

    

