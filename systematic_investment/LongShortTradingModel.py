#!/usr/bin/env python

"""
Provides LongShortTradingModel, a class for strategies involving long and short positions.

LongShortTradingModel extends TradingModel and implements calc_position_size and
calc_transaction_cost.
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

class LongShortTradingModel(TradingModel):
    def __init__(self, info, **kwargs):
        super(LongShortTradingModel, self).__init__(info, **kwargs)
        
    @staticmethod
    def calc_position_size(preds):
        tot = sum(abs(preds))
        return((preds)/tot)
        
    @staticmethod
    def calc_transaction_cost(positions):
        return(0.0)