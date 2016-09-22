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

from pandas import read_csv

def reg_create_func(info, **kwargs):
    """Returns a RegressionAnalyzer construction function.
    
    info: an Info object with a y_key field.
    
    kwargs: passed to RegressionAnalyzer
    
    """
    from systematic_investment.analysis import RegressionAnalyzer
    def res():
        df = read_csv(info.combined_df.path, index_col = [0,1], header=[0,1])
        return(RegressionAnalyzer(df, info.y_key, '2011-01-01', **kwargs))
    return(res)