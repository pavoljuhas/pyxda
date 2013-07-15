#!/usr/bin/env python

import numpy as np
import scipy as sp
import scipy.sparse as ssp
import fabio
import os
from traits.api import HasTraits, Instance, Int
from collections import deque

class ImageContainer(object):

    def __init__(self, n, imagename, dirpath):
        self.n = n
        self.imagename = imagename
        self.imagepath = dirpath + '/' + imagename
        self.imagedata = None
        #print self.imagepath
        return
        
class ImageCache(HasTraits, object):
    
    def __init__(self):
        self.cache = deque(maxlen=3)
        self.add_trait('imagepos', Int(-1))
        return
    
    def clean(self):
        self.cache.clear()
        self.imagepos = -1
        return
