#!/usr/bin/env python
# coding=utf-8
##############################################################################
#
# pyxda.srxes       X-ray Data Analysis Library
#                   (c) 2013 National Synchrotron Light Source II,
#                   Brookhaven National Laboratory, Upton, NY.
#                   All rights reserved.
#
# File coded by:    Michael Saltzman
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

from traits.api import HasTraits, Directory, Button, Int, Str, Enum
from traitsui.api import View, Item, Group, HGroup, VGroup, DirectoryEditor, \
                            TitleEditor, VGrid, UItem
from chaco import default_colormaps

class ControlPanel(HasTraits):
    '''Contains tools to interact with the data set.'''
    
    dirpath = Directory()
    left_arrow = Button('<')
    right_arrow = Button('>')
    reset = Button('Reset')
    generate = Button('Generate Reduced Representation Plot')
    dirpath = Directory()
    spacer = Str('  ')
    index = Int(0)
    of = Str('of')
    datalistlength = Int(0)
    spacer2 = Str('  ')
    colormap = Enum(default_colormaps.color_map_name_dict.keys())
    rrchoice = Enum('Choose a Reduced Representation', 'Total Intensity',
                'Mean', 'Standard Deviation', '% Pixels Below Threshold',
                '% Pixels Above Threshold')
    message = Str('')

    def _colormap_default(self): return 'jet'

    group = Group(
                UItem('dirpath', id='dirpath', 
                                        editor=DirectoryEditor(entries=5)),
                HGroup(
                    HGroup(
                        UItem('left_arrow'), 
                        UItem('right_arrow'),
                        padding = 5
                          ),
                    UItem('spacer', style='readonly'),
                    HGroup(
                        UItem('index', width=-30, height=-20),
                        UItem('of', style='readonly'),
                        UItem('datalistlength', style = 'readonly'),
                        padding = 5
                          ),
                    UItem('spacer2', style='readonly'),
                    UItem('colormap'),
                    padding = 5
                      ),
                VGroup(
                    UItem('rrchoice'),
                    UItem('generate'),
                      ),
                UItem('message', style='readonly'),
                show_border = True,
                )
    
    view = View(group, id='pyxda.srxes.cpanel')

class MetadataPanel(HasTraits):
    '''Contains metadata about the currently viewed image.'''
    
    name = Str('2D Image')
    height = Str('')
    width = Str('')
    qxrdVersion = Str('')
    qtVersion = Str('')
    dataType = Str('')
    dataTypeName = Str('')
    fileBase = Str('')
    fileName = Str('')
    title = Str('')
    readoutMode = Str('')
    summedExposures = Str('')
    imageNumber = Str('')
    phaseNumber = Str('')
    nPhases = Str('')
    dateTime = Str('')
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
    used = Str('')
    size = Str('')

    group = Group(
                UItem('name', editor=TitleEditor()),
                Group(
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
                        show_labels = True,
                        style = 'readonly',
                        columns = 2,
                        scrollable = True,
                        ),
                    show_labels = False,
                    show_border = True
                     )
                )

    view = View(group, height=150, width=700, resizable=True)

if __name__=='__main__':
    #ControlPanel().configure_traits()
    MetadataPanel().configure_traits()
