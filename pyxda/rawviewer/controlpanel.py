#!/usr/bin/env python
# -*- coding: utf-8 -*-

from traits.api import HasTraits, Directory, Button, Int, Str, Enum
from enthought.traits.ui.api import View, Item, Group, HGroup, HSplit, VGroup, \
                                    Heading, DirectoryEditor, TitleEditor, VFlow, \
                                    VGrid, UItem
from chaco.api import GridContainer

class ControlPanel(HasTraits):
    '''Contains tools to interact with image.'''
    
    dirpath = Directory()
    left_arrow = Button('<')
    right_arrow = Button('>')
    reset = Button('Reset')
    generate = Button('Generate Reduced Representation Map')
    dirpath = Directory()
    spacer = Str('              ')
    index = Int(0)
    of = Str('of')
    datalistlength = Int(0) 
    rrchoice = Enum('Choose a Reduced Representation', 'Total Intensity', 'Mean', 'Standard Deviation', 'Pixels Above Upper Bound', 'Pixels Below Lower Bound')
    filename = Str('')

    group = Group(
                Item('dirpath', editor=DirectoryEditor(), show_label=False),
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
                Item('rrchoice', show_label = False),
                Item('generate', show_label = False),
                UItem('filename', style = 'readonly'),
                show_border = True,
                )
    
    view = View(group)

# TODO: Organize the metadata.
class MetadataPanel(HasTraits):
    
    name = Str('2D Image')
    height = Str('')
    width = Str('')
    qxrdVersion = Str('')
    qtVersion = Str('')
    dataType = Str('')
    dataTypeName = Str('')
    fileBase = Str('')
    fileName = Str('')
    #D:/DataQXRD/data/120809X17A/LiRh2O4_w2k_082K-00007.tif')
    title = Str('')
    readoutMode = Str('')
    summedExposures = Str('')
    imageNumber = Str('')
    phaseNumber = Str('')
    nPhases = Str('')
    dateTime = Str('')
    #'@Variant(\\0\\0\\0\\x10\\0%zU\\x4\\xa6^\\x7f\\xff)')
    dateString=Str('')
    hBinning = Str('')
    vBinning = Str('')
    cameraGain = Str('')
    triggered = Str('')
    userComment1 = Str('')
    userComment2 = Str('')
    userComment3 = Str('')
    userComment4 = Str('')
    imageSaved = Str('')
    normalization = Str('')
    #'@Variant(\\0\\0\\0\\x7f\\0\\0\\0\\xfQcepDoubleList\\0\\0\\0\\0\\0)')
    used = Str('')
    size = Str('')

    group = Group(
                Item('name', editor=TitleEditor(), show_label=False),
                VGrid(
                    Item('height'),
                    Item('width'),
                    Item('qxrdVersion'),
                    Item('qtVersion'),
                    Item('dataType'),
                    Item('dataTypeName'),
                    Item('fileBase'),
                    Item('fileName'),
                    Item('title'),
                    Item('readoutMode'),
                    Item('summedExposures'),
                    Item('imageNumber'),
                    Item('phaseNumber'),
                    Item('nPhases'),
                    Item('dateTime'),
                    Item('dateString'),
                    Item('hBinning'),
                    Item('vBinning'),
                    Item('cameraGain'),
                    Item('triggered'),
                    Item('userComment1'),
                    Item('userComment2'),
                    Item('userComment3'),
                    Item('userComment4'),
                    Item('imageSaved'),
                    Item('normalization'),
                    Item('used'),
                    Item('size'),
                    show_border = True,
                    show_labels = True,
                    style = 'readonly',
                    columns = 3
                    )
                )

    view = View(group, resizable=True)

if __name__=='__main__':
    ControlPanel().configure_traits()
    #MetadataPanel().configure_traits()