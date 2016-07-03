#!/usr/bin/env python

"""
Provides utility methods.
"""

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
__status__ = "Development"

from pandas import read_csv
from numpy import abs, sign, median
from math import isnan
from scipy.stats import norm
import matplotlib.pyplot as plt

def identity(x):
    """Identity function."""
    return(x)

def read_csv_iso(path):
    """Read csv file with ISO-8859-1 encoding."""
    
    return read_csv(path, encoding = "ISO-8859-1")
    
def qd_bulk_downloader_func(info):
    from .QuandlBulkDBLoader import QuandlBulkDBLoader
    return(lambda: QuandlBulkDBLoader(info.downloaded_data.path))
    
def qd_downloader_func(info):
    """Returns a QuandlDBLoader constructor function.
    
    info: a Info object with an authtoken field.
    
    """
    from .QuandlDBLoader import QuandlDBLoader
    return(lambda: QuandlDBLoader(info.top().authtoken))
    
def reg_create_func(info, **kwargs):
    """Returns a RegressionAnalyzer construction function.
    
    info: an Info object with a y_key field.
    
    kwargs: passed to RegressionAnalyzer
    
    """
    from .RegressionAnalyzer import RegressionAnalyzer
    def res():
        df = read_csv(info.combined_df.path, index_col = [0,1], header=[0,1])
        return(RegressionAnalyzer(df, info.y_key, **kwargs))
    return(res)
    
def test_data_processing(info):
    """Tests data processing functionality.
    
    info: an Info object with settings information.
    
    """
    from .DataLoader import DataLoader
    
    dl = DataLoader(info.attr_dict())
    combiner = dl.load()
    return(combiner)
    
def test_models(info, action, *model_classes):
    """Tests models.
    
    info: an Info object with settings.
    
    action: what to do with the model.
    
    model_classes: constructors of models from info.
    
    """
    for model_class in model_classes:
        model = model_class(info)
        action(model)
    
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
    
def columns_compute_names(names, columns):
    """Returns second argument."""
    return(columns)
    
def names_compute_names(names, columns):
    """Returns first argument."""
    return(names)
    
def make_subplot():
    """Make a subplot."""
    return(plt.figure().add_subplot(1,1,1))
    
data_dir='data/'

from pandas import read_excel

def fix_read_excel(path, **kwargs):
    return(read_excel(data_dir+path, **kwargs))
    
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
    
def default_indicator_loader(path, loader=fix_read_excel):
    return(loader(path))
    
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

from pandas.core.base import FrozenList

def multi_idx_to_datetime(idx):
    return(idx.set_levels([idx.levels[0].to_datetime(), idx.levels[1]]))
    
def default_resample_method(data):
    return(data.resample('AS').pad())
    
def default_multi_index_resample_method(data):
    data.index = multi_idx_to_datetime(data.index)
    return(data) #fix this if necessary
    #gnames = [name for name in data.index.names if name != 'Date']
    #return(data.groupby(level=gnames).resample('AS').pad())