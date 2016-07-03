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
__status__ = "Development"

import pickle

class TradingModel:
    def __init__(self, info, **kwargs):
        """Creates a TradingModel object.
        
        info: an Info object with settings. 
        
        kwargs: passed to analyzer.analyze().
        
        """
        path_name = info.analyzer.path
        if info.analyzer.load:
            with open(path_name, "rb") as f:
                self.analyzer = pickle.load(f)
        else:
            y_name = info.y_key
            self.analyzer = info.analyzer.create()
            self.analyzer.analyze(y_name, path_name, **kwargs)
        
    def plot_historic_returns(self):
        """Plot historic returns of model."""
        self.analyzer.plot_model_returns(self.calc_position_size, self.calc_transaction_cost)
        
    def plot_hypothetical_portfolio(self):
        """Plot the hypothetical returns of a portfolio based off this model."""
        self.analyzer.plot_hypothetical_portfolio_returns(self.calc_position_size, self.calc_transaction_cost)
        
    def boxplots_by(self, by):
        """Make boxplots grouping by argument by.
        
        by: group by this argument.
        
        """
        self.analyzer.make_boxplots(by)
        
    def calc_position_size(self, preds):
        """Abstract method to compute position size from preds.
        
        preds: list of predictions.
        
        """
        raise(NotImplementedError("Please implement this function."))

    def calc_transaction_cost(positions):
        """Abstract method to compute transaction cost from positions.
        
        positions: list of trades.
        
        """
        raise(NotImplementedError("Please implement this function."))
        