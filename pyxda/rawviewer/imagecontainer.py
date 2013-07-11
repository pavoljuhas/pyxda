#!/usr/bin/env python

from collections import deque

class ImageContainer(object):

    def __init__(self, n, imagename, dirpath):
        self.n = n
        self.imagename = imagename
        self.imagepath = dirpath + '/' + imagename
        self.imagedata = None
        #print self.imagepath
        
class ImageCache(object):
    
    def __init__(self):
        self.cache = deque(maxlen=3)
        self.imagepos = -1
        return
    
    def clean(self):
        self.cache.clear()
        self.imagepos = -1
        return
