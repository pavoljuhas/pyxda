from enthought.traits.api import HasTraits,Int,Float,Str,Property
from enthought.traits.api import Range,Array, Instance 
from chaco.api import Plot, ArrayPlotData
import numpy as np

class Image():
    data = Instance(Array())
    plot = Instance(Plot())
    title = Str()
    headers = {} 
    
    def __init__(self, data, title, headers):
        self.data = data
        self.title = title
        self.headers = headers

