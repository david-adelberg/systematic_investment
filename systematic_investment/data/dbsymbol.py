#!/usr/bin/env python

"""
Provides DBSymbol, a class to represent a component of an API code.

DBSymbol holds a DataFrame of english names and codes. DBSymbol implements
methods methods to get the english names, to get the codes, and to create
an english-code dictionary.
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

class DBSymbol:
    def __init__(self, path, names_key, codes_key, loader=read_csv):
        """Creates a DBSymbol.
        
        path: load data from here.
        
        names_key: names column names in this column.
        
        codes_key: codes column names in this column.
        
        loader: function to get DataFrame from path.
        
        """
        self._df = loader(path)[[names_key, codes_key]]
        
    def english(self):
        """Gets the english names for the codes."""
        return self._df[self._df.columns[0]]
        
    def codes(self):
        """Get the codes in the symbol."""
        return self._df[self._df.columns[1]]
         
    def english_to_code_dictionary(self):
        """Get a dict mapping names to codes."""
        return dict(zip(self.english(), self.codes()))