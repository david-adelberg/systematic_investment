__author__ = "David Adelberg"
__copyright__ = "Copyright 2016, David Adelberg"
__credits__ = ["David Adelberg"]

__license__ = """May be used by members of the Yale College Student Investment
                 Group for education, research, and management of the  
                 organization's portfolio. All other uses require the express
                 permission of the copyright holder. Other interested persons
                 should contact the copyright holder."""
__version__ = "0.1.0"
__maintainer__ = "David Adelberg"
__email__ = "david.adelberg@yale.edu"
__status__ = "Prototype"

from scipy.stats import norm
from numpy import abs, sign, median
from math import isnan
import math

def identity(x):
    """Identity function."""
    return(x)
    
def transform_reduce_kurtosis(x, power):
    """Apply a power transformation centered at the median to reduce kurtosis.
    
    x: a list of data.
    
    power: the degree of the transformation.
    
    """
    med = median(x)
    return [sign(el)*abs(el-med)**power for el in x]
    
def transform_reduce_skewness(x, power):
    """Apply a power transformation centered at zero to reduce skewness.
    
    x: a list of the data.
    
    power: the degree of the transformation.
    
    """
    return [el**power for el in x]
    
def unif_to_normal(x):
    """Applies the inverse normal transformation to a series.
    
    x: a Series object.
    
    """
    def single(inp):
        if isnan(inp):
            return(inp)
        else:
            adj = 0.01
            inp *= 1-adj
            inp+= 0.5*adj
            return(norm.ppf(inp))
    return(x.apply(single))
    
def smart_divide(x,y, verbose=False):
    if y != 0:
        return(x/y)
    else:
        if verbose:
            print("x: ", x)
            print("y: ", y)
        return(math.nan)
