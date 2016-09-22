#!/usr/bin/env python

"""
Provides DBLoader, a class to load datasets from a file or from the internet.

DBLoader holds (down)loaded data, and defines methods to compute wanted api codes,
to download data, to load data, and to process data.
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

from pandas import DataFrame, read_csv, concat, to_datetime
import itertools
from numpy import array
from systematic_investment.shortcuts import identity, default_resample_method
from urllib.error import URLError

class DBLoader:
    def __init__(self, *args, **kwargs):
        """Creates a new DBLoader object.
        
        args: unused
        
        kwargs: unused
        
        """
        self._wanted_codes=None
        self._downloaded_data = None
        self._processed_data = None
        
    def load_all_codes(self, path, loader=read_csv):
        """Returns all codes from a path.
        
        path: codes are stored here.
        
        loader: function to load from path.
        
        """
        df = loader(path)
        return df[df.columns[0]].tolist()
        
    def load_wanted_codes(self, path, loader=read_csv):
        """Loads wanted codes from path.
        
        path: wanted codes are stored here.
        
        loader: function to load from path.
        
        """
        self._wanted_codes = loader(path)
    
    def compute_wanted_codes(self, code_builder, name_builder, symbols, path=None, all_valid_codes=None):
        """Computes wanted codes from symbols.
        
        code_builder: function mapping symbol codes to an API code.
        
        name_builder: function mapping symbol names to the english description
                        of an API code.
                        
        symbols: a list of DBSymbols.
        
        path: write wanted codes to this path.
        
        all_valid_codes: list of all codes that could be potentially called.
                            Used to exclude bad codes.
        
        """
        piece_code_lists = [symbol.codes() for symbol in symbols]
        piece_name_lists = [symbol.english() for symbol in symbols]
        computed_codes = [code_builder(*pc) for pc in itertools.product(*piece_code_lists)]
        computed_names = [name_builder(*pn) for pn in itertools.product(*piece_name_lists)]
        self._wanted_codes = DataFrame(array([computed_names, computed_codes]), index=['Name', 'Code']).transpose()
        if path is not None:
            self._wanted_codes.to_csv(path)
            
    def make_api_call(self, codes, **kwargs):
        """Makes an API call.
        
        codes: a list of API codes.
        
        """
        
        raise(NotImplementedError("Need to implement make_api_call"))
        
    def download_and_save(self, path, compute_names=identity, calls_per_iter=10, verbose=True, sindex=0, wanted_codes_name='Name', wanted_codes_code='Code', collapse="annual"):
        """Downloads and saves data.
        
        path: write downloaded data here.
        
        compute_names: function mapping columns to names.
        
        calls_per_iter: make this many API calls per iter (to avoid timeout).
        
        verbose: print status information?
        
        sindex: start with this code index, enabling recovery from interruptions.
        
        wanted_codes_name: Name column name in wanted_codes.
        
        wanted_codes_code: Code column name in wanted_codes.
        
        """
        downloads = []
        
        left_bound = sindex
        right_bound = sindex+calls_per_iter
        codes_len = len(self._wanted_codes.index.tolist())
        #names = self._wanted_codes[wanted_codes_name].tolist()
        codes = self._wanted_codes[wanted_codes_code].tolist()
        
        try:
            while left_bound < codes_len:
                if verbose:
                    print("Made %i/%i calls." % (min([codes_len, left_bound]), codes_len))
                dd = self.make_api_call(codes[left_bound:right_bound], collapse=collapse)
                dd.columns = compute_names(dd.columns) #names[left_bound:right_bound], 
                downloads.append(dd)
                left_bound = left_bound + calls_per_iter
                right_bound = right_bound + calls_per_iter
                
                if (left_bound % (calls_per_iter * 100)) == 0:
                    concat(downloads, axis=1).to_csv(path+'safety.csv')
                    print('used safety')
            if verbose:
                print("Successfully made %i/%i calls." % (codes_len, codes_len))
        except (URLError, TimeoutError):
            print("Error downloading.")
            print("%i successful calls" % left_bound)
            print("Attempting to recover from error. If this message repeats indefinately, terminate the program.")
            self.download_and_save(path, compute_names, calls_per_iter, verbose, left_bound, wanted_codes_name, wanted_codes_code)
            downloads.append(self._downloaded_data)
        except:
            all_downloaded_data = concat(downloads, axis=1)
            all_downloaded_data.to_csv(path+'backup.csv')
        else:
            all_downloaded_data = concat(downloads, axis=1)
            all_downloaded_data.to_csv(path)
            self._downloaded_data = all_downloaded_data
        
    def load_downloaded_data(self, path, load=lambda p: read_csv(p, index_col=0)):
        """Loads downloaded data.
        
        path: data is stored here.
        
        load: a function to read from the path.
        
        """
        self._downloaded_data=load(path)
        
    def process(self, path, compute_names, english_to_symbol_indicator,
                indicator_handler, symbol_name, date_name='Date',
                resample_method=default_resample_method, idx_to_datetime=to_datetime, **kwargs):
        """Processes data.
        
        path: write processed data here.
        
        compute_names: maps column names to computed_names.
        
        english_to_symbol_indicator: split english names into symbol and indicator.
        
        indicator_handler: function to handle indicators 
                            (e.g. compute previous/future pct change)
                            
        symbol_name: name key for symbol (security)
        
        resample_method: How to resample?
        
        """
        
        data = self._downloaded_data
        data.dropna(axis=1, how='all', inplace=True)
       # data.set_index(date_name, drop=True, inplace=True)
        data.index = idx_to_datetime(data.index)
        if resample_method is not None:
            data = resample_method(data)
        
        data.columns = compute_names(data.columns)
        cols = list(data.columns)
        indices = list(data.index)
        
        vals = {}
        ldata = data.values.tolist()
        
        for col_idx, col in enumerate(cols):
            symbol, indicator = english_to_symbol_indicator(col)
            for row_idx, date in enumerate(indices[1:-1]):
                key = {symbol_name: symbol, date_name: date}
                
                to_update = {indicator: ldata[row_idx][col_idx]}
                to_update.update(indicator_handler(indicator, ldata[row_idx-1][col_idx], ldata[row_idx][col_idx], ldata[row_idx+1][col_idx]))
                frozen_key = frozenset(key.items())
                if frozen_key in vals:
                    vals[frozen_key].update(to_update)
                else:
                    vals[frozen_key] = to_update
        
        data_as_list_of_dicts = []
        for country_date, indicators in vals.items():
            to_append = {}
            to_append.update(country_date)
            to_append.update(indicators)
            data_as_list_of_dicts.append(to_append)
            
        self._processed_data = DataFrame(data_as_list_of_dicts)
        self._processed_data.set_index([date_name, symbol_name], inplace=True, drop=True)
        self._processed_data.to_csv(path)
        
    def get_processed_data(self):
        """Gets processed data."""
        return self._processed_data