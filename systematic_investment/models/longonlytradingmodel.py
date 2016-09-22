#!/usr/bin/env python

"""
Provides LongOnlyTradingModel, a class for strategies only involving long positions.
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

from .tradingmodel import TradingModel

class LongOnlyTradingModel(TradingModel):
    
    def __init__(self, info):
        super(LongOnlyTradingModel, self).__init__(info)
        
    @staticmethod
    def calc_position_size(preds):
        preds[preds<0.0] = 0.0
        return(preds / preds.abs().sum())
        
    @staticmethod
    def calc_transaction_cost(positions):
        return(0.0)