#!/usr/bin/env python

"""
In progress

Provides QuandlBulkDBLoader, a class for loading bulk data from Quandl.
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
__status__ = "Prototype"

from systematic_investment.data.dbloader import DBLoader
from pandas import read_csv, DataFrame
from systematic_investment.shortcuts import *

class QuandlBulkDBLoader(DBLoader):
    
    def __init__(self, *args, **kwargs):
        """Creates a QuandlBulkDBLoader object.

        path: path to bulk downloaded data        
        
        args: unused.
        
        kwargs: unused.
        
        """
        
        super(QuandlBulkDBLoader, self).__init__(self)
        
    def make_api_call(self, codes):
        """Make API calls.
        
        codes: list of API codes.
        """
        raise(NotImplementedError("make_api_call does not have meaning."))
        
    def load_downloaded_data(self, path):
        self._downloaded_data = read_csv(path, index_col=False)
        
    def download_and_save(self, path, compute_names=identity, english_to_symbol_indicator=default_english_to_symbol_indicator, verbose=True, wanted_codes_name='Name', wanted_codes_code='Code', *args, **kwargs):
        self.load_downloaded_data(path)
        
    def process(self, path, compute_names, english_to_symbol_indicator,
                indicator_handler, symbol_name, date_name='Date',
                resample_method=default_multi_index_resample_method, idx_to_datetime=multi_idx_to_datetime):
            """Processes data.
            
            path: write processed data here.
            
            compute_names: maps column names to computed_names.
            
            english_to_symbol_indicator: split english names into symbol and indicator.
            
            indicator_handler: function to handle indicators 
                                (e.g. compute previous/future pct change)
                                
            symbol_name: name key for symbol (security)
            
            resample_method: How to resample?
            
            """
            
            res = {}
            self._processed_data = self._downloaded_data
            self._processed_data['Code'] = compute_names(self._processed_data['Code'])
            for row in self._processed_data.index:
                sym, ind = english_to_symbol_indicator(self._processed_data['Code'].loc[row])
                date = self._processed_data['Date'].loc[row]
                val = self._processed_data['Value'].loc[row]
                try:
                    if ind != "Missing":
                        res[date, sym][ind] = val
                except:
                    res[date, sym] = {ind: val}
                 
            df = DataFrame.from_dict(res)
            df = df.transpose()
            self._processed_data = df            
            self._processed_data.index.names=['Date', 'Security']
            self._processed_data.to_csv(path)