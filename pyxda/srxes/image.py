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

import numpy as np
import fabio
import os
from traits.api import HasTraits, Instance, Int
from collections import deque

class Image(object):
    '''An object that contains relevant information about a .tif image.

    Each image has a name, filepath, n (index), data, and metadata.
    Dummy images can be created as placeholders. They only have a name
    (2D Image), blank metadata, n (-1), and data. They are instantiated if
    the initialized path is an empty string.
    '''

    def __init__(self, n, path):
        if path == '':
            self.name = '2D Image'
            self.metadata = {}
            self.n = -1
            self.data = None
            return
        self.name = os.path.split(path)[1]
        self.path = path
        print path
        self.n = n
        self.data = None
        self.metadata = self._parseMD()
        return

    def _parseMD(self):
        '''Opens the associated .metadata file and parses the information.

        If no such file exists, the metadata is left empty.
        '''
        md = {}
        try:
            fp = open(self.path+'.metadata', 'rU')
            for i, line in enumerate(fp):
                line = line.rstrip('\n')
                if line == '' or line[0] == '[':
                    continue
                words = line.split('=', 1)
                md[words[0]] = str(words[1])
            fp.close()
        except IOError:
            pass
        return md

    def load(self):
        '''Loads data from the .tif file and stores it in a numpy array.'''
        if self.data is None and self.n != -1:
            fo = fabio.open(self.path)
            self.data = fo.data
        return

class ImageCache(HasTraits, object):
    '''An image cache that contains at most 3 Image objects.

    The cache ensures that 3 images are loaded into memory at a given time.
    These include the current, next, and previous images. This allows 
    faster plotting of images. The cache is a deque of size 3 with modified
    pop/append methods.
    '''
    
    def __init__(self):
        self.cache = deque(maxlen=3)
        for i in range(3):
            self.cache.append(Image(-1, ''))
        return

    def __str__(self):
        '''Provides a string representation for the ImageCache.

        Image Cache:
        index of 1st image
        index of 2nd image
        index of 3rd image
        '''
        temp1 = self.cache.popleft()
        temp2 = self.cache.popleft()
        temp3 = self.cache.popleft()
        s1 = 'Image Cache:\n%d\n%d\n%d' % (temp1.n, temp2.n, temp3.n)
        self.cache.append(temp1)
        self.cache.append(temp2)
        self.cache.append(temp3)
        return s1

    def append(self, image):
        '''Appends the new image and deloads the image that is removed.'''
        temp = self.cache.popleft()
        if temp.n is not -1:
            temp.data = None
        self.cache.append(image)
        image.load()
        return

    def appendleft(self, image):
        '''Appends left the new image and deloads the image that is removed.'''
        temp = self.cache.pop()
        if temp.n is not -1:
            temp.data = None
        self.cache.appendleft(image)
        image.load()
        return

    def pop(self):
        '''Pops an Image from the right and places a dummy image on left.'''
        temp = self.cache.pop()
        self.cache.appendleft(Image(-1, ''))
        return temp

    def popleft(self):
        '''Pops an Image from the left and places a dummy image on right.'''
        temp = self.cache.popleft()
        self.cache.append(Image(-1, ''))
        return temp

    def reverse(self):
        '''Reverses the cache.'''
        self.cache.reverse()
        return

    def clear(self):
        '''Deloads the current images, and replaces them with dummy Images.'''
        while True:
            try:
                self.cache.pop().data = None
            except IndexError:
                break
        for i in range(3):
            self.cache.append(Image(-1, ''))
        return
