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

from sklearn.linear_model import LassoLarsCV
from pandas import Series, DataFrame

class SKLearnInterop:
    def __init__(self, lm_y, lm_x, constructor):
        self._lm_x = lm_x
        self._lm_y = lm_y
        self._obj = constructor()
        self._score = None
        
    def summary(self, xname, yname):
        coefs_to_print = DataFrame(self._obj.coef_)
        coefs_to_print.index = xname
        coefs_to_print.columns = (yname,)
        
        intercept_to_print = Series(self._obj.intercept_)
        intercept_to_print.index=(yname,)
        
        score_to_print = self._obj.score(self._lm_x, self._lm_y)
        self._score = score_to_print
        
        return("Coefficients:\n%s\nIntercepts:\n%s\nR^2:\n%s" % 
            (coefs_to_print, intercept_to_print, score_to_print))
        
    def fit(self):
        self._obj.fit(self._lm_x, self._lm_y)
        self._obj.__setattr__('summary', self.summary)
        return(self._obj)

def lasso_constructor(y,x):
    return(SKLearnInterop(y,x, LassoLarsCV))