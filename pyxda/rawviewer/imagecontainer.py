import numpy as np
import scipy as sp
import scipy.sparse as ssp
import fabio
import os

from collections import deque

class ImageContainer(object):

    def __init__(self, n, imagename, dirpath):
        self.n = n
        self.imagename = imagename
        self.imagepath = dirpath + '/' + imagename
        self.imagedata = None
        print self.imagepath
        
    def getImageData(self):
        fo = fabio.open(self.imagepath)
        return fo.data
        
class ImageCache(object):
    
    def __init__(self):
        self.cache = deque()
        self.imagepos = -1
        return
    
    def clean(self):
        self.cache.clear()
        self.imagepos = -1
        return
