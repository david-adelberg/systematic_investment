#!/usr/bin/env python

"""
Provides DFAnalyzer, an abstract class for the analysis of a statistical model.

DFAnalyzer holds a DataFrame and the name of the y column(s) and implements
methods for data visualization, model fitting, and strategy performance visualization.
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

from systematic_investment.shortcuts import make_subplot, plot_returns
from scipy.stats import zscore, probplot
from pandas import concat
import pickle

class DFAnalyzer:
    def __init__(self, df, y_key, pred_col_name='Predicted Z-score for transformed percent change', pos_col_name ='Strategy position', net_profit_name ='Net Profit', drop_observations=True):
        """Returns new DFAnalyzer object with specified DataFrame and y key.
        
        df: the DataFrame of data to analyze.
        
        y_key: the dependent variable(s).
        
        pred_col_name: column name for predicted values.
        
        pos_col_name: column name for positions.
        
        net_profit_name: column name for net profit.
        
        """
        
        self._original_df = df
        self._to_analyze = df
        self._y_key = y_key
        
        self.pred_col_name = [pred_col_name]
        self.pos_col_name = pos_col_name
        self.net_profit_name = net_profit_name
        
        self.drop_na_y_key()
        if drop_observations:
            self.drop_observations()
        
    def drop_na_y_key(self):
        """Drops all rows with a NA in the y key."""
        if self._y_key.__class__ == list:
            for key in self._y_key:
                self._to_analyze.dropna(subset=[key], inplace=True)
        else:
            self._to_analyze.dropna(subset=[self._y_key], inplace=True)
        
    def drop_observations(self, min_pct_change=-40.0, max_pct_change=40.0):
        """Drops all observations outside of [min_pct_change, max_pct_change]
        
        min_pct_change: minimum percent change to keep
        
        max_pct_change: max_percent_change to keep.
        """
        
        is_good = (self._to_analyze[self._y_key] > min_pct_change) & (self._to_analyze[self._y_key] < max_pct_change)
        goods = self._to_analyze.loc[is_good].index
        self._to_analyze = self._to_analyze.loc[goods]
        
    def add_transformation(self, *args, **kwargs):
        """Applies a transformation to self._to_analyze.
        
        args: a function followed by column names corresponding to arguments.
        
        drop_old (optional): drop old column?
        
        name (optional): new column name
        
        whole_list (optional): apply function to entire column list or just one entry?
        
        y_key (optional): y_key.
        
        """
        func = args[0]
        lkeys = list(args[1:])
        
        name = None
        
        if "name" in kwargs:
            name = kwargs["name"]
        else:
            name = lkeys[0] + " - Transformed_"
            
        input_list = self._to_analyze[lkeys].values.tolist()
        
        if "whole_list" in kwargs and kwargs["whole_list"]:
            res = func(input_list)
            self._to_analyze[name] = res
        else:
            self._to_analyze[name] = [func(*args) for args in input_list]
        
        if not ("drop_old" in kwargs and not kwargs["drop_old"]):
            self._to_analyze.drop(lkeys[0], axis=1, inplace=True)
            
    def compute_name(self, *args):
        """Computes column name from args.
        
        args: function name followed by argument names.
        
        """
        return '(%s)(%s)' % (args[0], ', '.join(args[1:]))
            
    def make_transformations(self, list_of_transform_args, drop_old=True):
        """Apply list of transformations to self._to_analyze.
        
        list_of_transform_args: list of iterables of arguments to add_tranformation.
        
        drop_old: drop old columns?
        
        """
        for t_arg in list_of_transform_args:
            args = [eval(t_arg[0])] + list(t_arg[1:])
            name = self.compute_name(*t_arg)
            
            #'(%s)(%s)' % (t_arg[0], ', '.join(t_arg[1:]))
            self.add_transformation(*args, drop_old=drop_old, name=name)
            
    def make_univariate_plot(self, col_name, plot_type=['hist', 'boxplot', 'probplot']):
        """Makes univariate plot for col_name.
        
        col_name: name of column to analyze
        
        plot_type: list of types of plots to make.
        
        """
        data = self._to_analyze[col_name].dropna().tolist()
        if 'hist' in plot_type:
            splt = make_subplot()
            splt.hist(data)
            splt.set_xlabel(col_name)
        if 'boxplot' in plot_type:
            splt = make_subplot()
            splt.boxplot(data)
            splt.set_xlabel(col_name)
        if 'probplot' in plot_type:
            splt = make_subplot()
            probplot(data, dist="norm", plot=splt)
            splt.set_xlabel(col_name)
            
    def make_univariate_plots(self, plot_type=['hist']):
        """Make univariate plots for all columns.
        
        plot_type: list of types of plots to make.
        
        """
        for col_name in self._to_analyze.columns:
            self.make_univariate_plot(col_name, plot_type=plot_type)

    def get_outliers(self, y_key):
        """Gets outliers in y_key (|z|>3)
        
        y_key: column to study.
        
        """
        
        data = concat([self._to_analyze[self._to_analyze], self._to_analyze[y_key]], axis=1).dropna(subset=[y_key])
        is_outlier = abs(zscore(data[y_key])) > 3
        return data[is_outlier]
        
    def analyze(self, y_key, path, *args, **kwargs):
        """Fit statistical model and save.
        
        y_key: dependent variable(s).
        
        path: save self here.
        
        args: pass to analyze_impl.
        
        kwargs: pass to analyze_impl.
        
        """
        self.analyze_impl(y_key, *args, **kwargs)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        
    def analyze_impl(self, y_key, *args, **kwargs):
        """Method to perform analysis.
        
        y_key: dependent variable column name(s).
        
        args: user-defined meaning.
        
        kwargs: user-defined meaning.
        
        """
        raise(NotImplementedError("Please implement this method."))
        
    def load(path):
        """Load DFAnalyzer from path.
        
        path: DFAnalyzer stored here.
        
        """
        pickle.load(path)

    def print_analysis_results(self, *args, **kwargs):
        """Prints results of analysis.
        
        args: user-defined
        
        kwargs: user-defined.
        
        """
        raise(NotImplementedError("Please implement this method."))
        
    def plot_analysis_results(self, *args, **kwargs):
        """Plots results of analysis.
        
        args: user-defined.
        
        kwargs: user-defined.
        
        """
        raise(NotImplementedError("Please implement this method."))
    
    def compute_model_positions(self, *args, **kwargs):
        """Computes model positions.
        
        args: user-defined.
        
        kwargs: user-defined.
        
        """
        raise(NotImplementedError("Please implement this method."))
        
    def compute_model_returns(self, calc_position_size, calc_transaction_cost):
        """Computes strategy returns by year.
        
        calc_position_size: method to compute position size.
        
        calc_transaction_cost: method to compute associated transaction cost.
        
        """
        df = self.compute_model_positions(calc_position_size)
        costs = df[self.pos_col_name].apply(calc_transaction_cost)
        pct_changes = self._to_analyze[self._y_key]
        gross_trading_profits = pct_changes.multiply(df[self.pos_col_name], axis=0)
        net_trading_profit = gross_trading_profits.subtract(costs, axis=0)
        net_trading_profit.name=self.net_profit_name
        combined = concat([df, net_trading_profit], axis=1)
        grouped = combined.groupby(axis=0, level=combined.index.names.index('Date'))
        returns = grouped[self.net_profit_name].sum()
        returns.name = 'Strategy returns by year (%)'
        return(returns)
        
    def plot_model_returns(self, calc_position_size, calc_transaction_cost, live_date=None):
        """Plots model returns by year.
        
        calc_position_size: method to compute position sizes.
        
        calc_transaction_cost: method to compute transaction costs.
        
        """
        returns = self.compute_model_returns(calc_position_size, calc_transaction_cost)
        plot_returns(returns, live_date)
        
    def plot_hypothetical_portfolio_returns(self, calc_position_size, calc_transaction_cost, live_date=None):
        """Plot returns of a hypothetical portfolio over the lifetime of the model.
        
        calc_position_size: method to compute position size
        
        calc_transaction_cost: method to compute associated transaction cost.
        
        """
        returns = self.compute_model_returns(calc_position_size, calc_transaction_cost)
        compounded = (1.0 + (returns / 100.0)).cumprod()
        plot_returns(compounded, live_date)
        
    def make_boxplots(self, by):
        """Method to make boxplots for groupings by argument by.
        
        by: group by this to make boxplots.
        
        """

        df = self._original_df[self._y_key].dropna()
        title = self._y_key
        shortcuts.make_boxplots(df, by, title)