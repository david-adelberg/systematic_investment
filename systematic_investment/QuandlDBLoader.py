#!/usr/bin/env python

"""
Provides QuandlDBLoader, a class for downloading data from Quandl.

QuandlDBLoader holds an authtoken implements make_api_call.
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

from .DBLoader import DBLoader
import Quandl as qd

class QuandlDBLoader(DBLoader):
    
    def __init__(self, authtoken, *args, **kwargs):
        """Creates a QuandlDBLoader object.
        
        authtoken: authtoken to use.
        
        args: unused.
        
        kwargs: unused.
        
        """
        super(QuandlDBLoader, self).__init__(self)
        self._authtoken = authtoken
        
    def make_api_call(self, codes, **kwargs):
        """Make API calls.
        
        codes: list of API codes.
        """
        return(qd.get(codes, authtoken=self._authtoken, **kwargs))