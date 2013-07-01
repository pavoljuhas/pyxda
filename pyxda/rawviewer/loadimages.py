import os
import numpy as np
import re
import fabio
from enthought.traits.api import Dict, Instance

def getTiffImages(directory):
    # TODO: Change to single file loading.
    '''Reads in the tiff images from a select folder.
    

    directory -- The directory of the files to be imported, '.tiff' only.

    Returns a list of fabio objects, which contains a numpy array for
    the datasets and a dictionary for their headers for each tiff image.
    '''


    filelist = os.listdir(directory)
    tifflist = []                                           
    output = Instance(Dict)
    
    
    # Creates a list of .tiff files
    for f in filelist:
        #if f[int('-%d' % len("tiff")):] == "tiff":
        if f[-4:] == "tiff" or f[-3:] == "tif":
            tifflist.append(f)
    
    output = {}
    # Creates a list of fabio objects for each image
    for i, f in enumerate(tifflist):
        if i == 5:
            return output
        fo = fabio.open(directory + f)
        output[f] = fo
    
    return output


if __name__ == '__main__':
    dirpath = '/Users/Mike/Downloads/1208NSLSX17A_LiRh2O4/'
    output = getTiffImages(dirpath)
    print output


