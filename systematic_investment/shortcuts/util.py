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

from math import isnan
from pandas import concat, to_datetime

def columns_compute_names(names, columns):
    """Returns second argument."""
    return(columns)
    
def names_compute_names(names, columns):
    """Returns first argument."""
    return(names)
    
def make_default_code_builder(db):
    def res(first, *additional):
        to_ret = "%s/%s" % (db, first)
        for n_val in additional:
            to_ret += "_%s" % n_val
        
        return(to_ret)
    
    return(res)
    
def default_name_builder(first, *additional):
    res = first
    for val in additional:
        res += ": %s" % val
        
    return(res)
    
def make_default_compute_names(special_cols, col_handler):
    def res(columns):
        ncolumns = []
        for col in columns:
            if col in special_cols:
                ncolumns.append(col)
            else:
                ncolumns.append(col_handler(col))
        
        return(ncolumns)
    return(res)
    
def default_english_to_symbol_indicator(english):
    sp = english.split(' - ')
    symbol = sp[0]
    ind = sp[1]
    return symbol, ind
    
def make_default_indicator_handler(to_handle, future_looking):
    def handler(indicator, prev_val, current_val, next_val):
        res= {}
        key = "Percent change in %s" % indicator
        if indicator in to_handle:
            
            if isnan(prev_val) or isnan(current_val) or prev_val==0.0 or next_val==0.0:
                res.update({key: float('nan')})
            else:
                percent_change = ((current_val - prev_val) / prev_val)*100.0
                res.update({key: percent_change})
        
        if indicator in future_looking:
            key = "Future " + key
            
            if isnan(current_val) or isnan(next_val) or current_val==0.0 or next_val==0.0:
                res.update({key: float('nan')})
            else:
                percent_change = ((next_val - current_val) / current_val)*100.0
                res.update({key: percent_change})
        return(res)
    return(handler)

def multi_idx_to_datetime(idx):
    return(idx.set_levels([idx.levels[0].to_datetime(), idx.levels[1]]))
    
def default_resample_method(data):
    return(data.resample('AS'))#.pad())
    
def default_multi_index_resample_method(data):
    data.index = multi_idx_to_datetime(data.index)
    data = data.unstack().resample('AS').stack()
    return(data) #fix this if necessary. Did a potential fix.
    #gnames = [name for name in data.index.names if name != 'Date']
    #return(data.groupby(level=gnames).resample('AS').pad())
    
def default_combine_func(transformed_dfs):
    return(concat(transformed_dfs.values(), axis=1, keys=transformed_dfs.keys()))