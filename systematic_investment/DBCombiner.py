#!/usr/bin/env python

"""
Provides DBCombiner, a class to combine multiple datasets

DBCombiner holds a dict of DataFrames, and defines a combine method and
methods to drop columns by name or by proportion NA.
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

from pandas import concat, DataFrame
from .shortcuts import identity

class DBCombiner:
    def __init__(self, consolidated_dfs):
        """Returns a new DBCombiner object with specificed processed DataFrames.
        
        consolidated_dfs: a dict of DataFrames.
        
        """
        
        self._dfs = {name: df.sort_index() for (name, df) in consolidated_dfs.items()}
        self._combined = None
    
    def combine(self, to_drop = [], combined_names = [None, None], max_na_prop=0.9, path='test_combine.csv', transformer=identity):
        """Combines DataFrames.
        
        to_drop: a list of columns to drop.
        
        combined_names: Names of levels of combined columns.
        
        max_na_prop: Remove columns with more than this proportion NA.
        
        path: write the combined DataFrame to this path.
        
        transformer: a function mapping a DataFrame to a transformed DataFrame.
        
        """
        transformed_dfs = {key: transformer(df) for key, df in self._dfs.items()}
        self._combined = concat(transformed_dfs.values(), axis=1, keys=transformed_dfs.keys())
        self.drop_cols(to_drop)
        self.rm_cols(max_na_prop)
        self._combined.columns.rename(combined_names, inplace=True)
        self._combined.to_csv(path)
        return(self)
        
    def drop_cols(self, to_drop):
        """Drops columns in to_drop.
        
        to_drop: a list of columns to drop.
        
        """
        self._combined.drop(to_drop, level=0, axis=1, inplace=True)
        
    def get_col_na_props(self):
        """Returns a DataFrame of proportion NA by column.
        """
        res = []
        for name, vals in self._combined.iteritems():
            prop_na = vals.isnull().mean()
            res.append({"Indicator": name, "Proportion NA": prop_na})
        res = sorted(res, key=lambda x: x['Proportion NA'], reverse=True)
        df = DataFrame(res)
        df.set_index('Indicator', inplace=True, drop=True)
        return(df)
        
    def rm_cols(self, max_na_prop=0.95):
        """Removes columns with too many NAs.
        
        max_na_prop: maximum acceptable proportion NA.
        
        """
        
        na_props = self.get_col_na_props()
        selection = na_props.index[(na_props < max_na_prop)['Proportion NA'].tolist()]
        self._combined = self._combined[selection.tolist()]
        return(self)
        