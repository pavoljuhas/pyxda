import numpy as np

def integrate(picture):
    '''2D Integration Function
    Takes in a numpy array as an argument.
    Returns the sum of all the elements in the array.
    Will only work on numpy arrays'''
    
    summation = picture.sum()
    return summation
 
#For Testing   
if __name__ == '__main__':
    summation = integrate(np.arange(10))
    print summation