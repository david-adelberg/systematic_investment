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
import pandas as pd

class MultiModel:
    
    def __init__(self, models, split_date=None, **kwargs):
        self._models = models
        self._split_date = split_date
        self.run_analyses()
        
    def compute_returns_by_period(self):
        return({key: m.compute_returns_by_period() for key, m in self._models.items()})
        
    def compute_model_returns(self):
        returns_arr = []
        for name, model in self._models.items():
            m_rets = model.analyzer.compute_model_returns(model.calc_position_size, model.calc_transaction_cost)
            returns_arr.append(m_rets)
        
        returns_df = pd.concat(returns_arr, axis=1)
        overall_returns = returns_df.mean(axis=1)
        return(overall_returns)
        
    def summarize(self):
        names = []
        lengths = []
        scores = []
        for name, m in self._models.items():
            names.append(name)
            lengths.append(m.analyzer._data_len)
            scores.append(m.analyzer._obj._score)
        
        res = pd.DataFrame([names, lengths, scores]).T
        res.columns = ["Name", "# of Training Data Points", "Score"]
        return(res)
        
    def print_models(self):
        print(self.summarize().sort_values(['Score'], ascending=False))
        
    def plot_model_returns(self):
        plot_returns(self.compute_model_returns(), self._split_date)
        
    def plot_hypothetical_portfolio(self):
        returns = self.compute_model_returns()
        compounded = (1.0 + (returns / 100.0)).cumprod()
        plot_returns(compounded, self._split_date)
        
    def run_analyses(self):
        return({name: model.get_analysis_results() for name, model in self._models.items()})
        
    def print_analysis_results(self):
        for sector, model in self._models.items():
            print("Sector: %s" % sector)
            model.print_analysis_results()
            
    def drop_bad_models(self, keep_crit):
        self._models = {key: model for key, model in self._models.items() if keep_crit(model)}
        
def multi_model_create_info_interop(info, split_date, **kwargs):
    return(MultiModel(info._models, split_date, **kwargs))
        
        