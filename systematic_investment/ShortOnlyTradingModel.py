#!/usr/bin/env python

"""
Provides ShortOnlyTradingModel, a class for strategies with only short positions.

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

from systematic_investment import TradingModel

class ShortOnlyTradingModel(TradingModel):
    
    def __init__(self, info):
        super(ShortOnlyTradingModel, self).__init__(info)
        
    @staticmethod
    def calc_position_size(preds):
        preds[preds>0.0] = 0.0
        tot = sum(abs(preds))
        return((preds)/tot)
        
    @staticmethod
    def calc_transaction_cost(positions):
        return(0.0)