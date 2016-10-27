#!/usr/bin/env python

"""
Provides TradingModel, an abstract class to study the performance of trading strategies and statistical models.

TradingModel holds a subclass of DFAnalyzer, and implements methods to visualize
the data and to visualize simulated strategy performance. 
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

import numpy as np
from systematic_investment.shortcuts import plot_returns

class MultiModel:
    
    def __init__(self, models, split_date=None, **kwargs):
        self._models = models
        self._split_date = split_date
        
    def compute_model_returns(self):
        returns_arr = []
        for name, model in self._models:
            m_rets = model.analyzer.compute_model_returns(model.calc_position_size, model.calc_transaction_cost)
            returns_arr.append(m_rets)
            
        returns_arr = np.array(returns_arr)
        overall_returns = returns_arr.mean(axis=0) # Need to check this, probably wrong
        return(overall_returns)
        
    def plot_model_returns(self):
        plot_returns(self.compute_model_returns(), self._split_date)
        
    def plot_hypothetical_portfolio_returns(self):
        returns = self.compute_model_returns()
        compounded = (1.0 + (returns / 100.0)).cumprod()
        plot_returns(compounded, self._split_date)
        
def multi_model_create_info_interop(info, split_date, **kwargs):
    return(MultiModel(info.models, split_date, **kwargs))
        
        