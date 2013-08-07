import os
import numpy as np
import re

# TODO: Modified on 08/05/13 in order to test new waterfall plot.
def getDataSets(ext):
    '''Reads in data from the 'T_depdent_data' folder.
    
    Must be run in the directory containing 'T_depdent_data'. Creates a dictiona    ry with keys that indicate the temperature for the data set. Each dictionary    entry is organized into a list with elements. The first element is a list of    the x values and the second element is a list of the y values.

    ext -- The extension of the files to be imported, '.chi' only.

    Returns a numpy array containing the data, organized as specified above.
    '''

    SKIPBEG = 53
    SKIPEND = 10

    path = '/Users/Mike/waterfall-plot/T_depdent_data'


    filelist = os.listdir(path)
    chilist = []                                           
    output = []

    # Creates a list of .chi files
    for f in filelist:
        if f[int('-%d' % len(ext)):] == ext:
            chilist.append(f)
            
    # Creates a regular expression pattern to find temps in file names.
    p = "\d{3}"
    patt = re.compile(p)
    
    # Creates dictionary entries for each dataset.
    for f in chilist:
        match = re.search(patt, f)
        if match:
            data = np.genfromtxt(path + '/' + f,
                              skip_header=SKIPBEG, skip_footer=SKIPEND)
            data = data[::2]
            data = np.transpose(data)
            data = np.array(data)
            output.append(data)
    
    return output

if __name__ == "__main__":
    a = getDataSets('.chi')
    for set in a:
        print set[1]
