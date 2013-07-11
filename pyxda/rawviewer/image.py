from enthought.traits.api import Str
from enthought.traits.api import Array, Instance 
from chaco.api import Plot

class Image():
    data = Instance(Array())
    plot = Instance(Plot())
    title = Str()
    headers = {} 
    
    def __init__(self, data, title, headers):
        self.data = data
        self.title = title
        self.headers = headers

