#!/usr/bin/env python

"""
Provides RegressionModel, a class to fit and study linear regression models.

RegressionModel holds _lm_x, _lm_y, and _lm, objects for regression independent variables,
dependent variable, and the statistical model object. The class implements
methods to fit the model and visualize the results.
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

from pandas import DataFrame, concat
from sklearn.preprocessing import Imputer, LabelEncoder
from sklearn import linear_model
import statsmodels.api as sm
from statsmodels.tools.tools import categorical
import pickle
from .dfanalyzer import DFAnalyzer
from systematic_investment.shortcuts import *
import numpy as np

from systematic_investment.shortcuts import unif_to_normal

class RegressionAnalyzer(DFAnalyzer):
    def __init__(self, df, y_key, split_date, constructor=sm.OLS, **kwargs):
        """Creates a RegressionAnalyzer.
        
        df: DataFrame to analyze.
        
        y_key: name of dependent variable(s).
        
        kwargs: passed to DFAnalyzer
        
        """
        super(RegressionAnalyzer, self).__init__(df, y_key, **kwargs)
        
        self._lm_x = None
        self._lm_y = None
        self._lm = None
        self._obj = None
        self._split_date = split_date
        self._constructor=constructor
        self._data_len = None
        self._summary = None

    def get_lm_y_x(self, y_key, data):
        lm_y = data[y_key]
        drop_y = data.drop(y_key, axis=1)

        to_impute = drop_y.select_dtypes(include=[np.number])
        others = drop_y.select_dtypes(exclude=[np.number])
        #others_matrix = categorical(others.values, col=0, drop=True) # Fix later when necessary
        #others_matrix = categorical(others.values)
        
        #others_array = [LabelEncoder().fit_transform(others[col_name]) for col_name in others.columns]
        #others_array = np.asarray(others_array).T
        #others = DataFrame(others).T
        
        imp_inp = to_impute.values.tolist()
        lm_x = Imputer(strategy='median').fit_transform(imp_inp)
        lm_x = np.concatenate([lm_x, others], axis=1)#others_matrix
        #df_x = DataFrame(lm_x)
        #df_x.index = to_impute.index
        #df_x.columns = to_impute.columns
        #lm_x = concat([lm_x, others_array], axis=1).values.tolist() #df_x, others
        return(lm_y, lm_x)
            
    def analyze_impl(self, y_key, normals=True, path='model.pickle', *args, **kwargs):
        """Performs regression analysis.

        y_key: the y key.

        constructor: creates self._lm from self._lm_y and self._lm_x.
        
        normals: Apply inverse normal transform to normalize data?
        
        path: store model here.
        
        args: unused.
        
        kwargs: split_date: split into training and test here.
        
        """
        self._y_key = y_key
        data = self._to_analyze#.dropna(subset=[self._y_key], axis=1)
            
        if normals:
            ranked = data.select_dtypes(include=[np.number])
            ranked = ranked.rank(pct=True).apply(unif_to_normal)
            others = data.select_dtypes(exclude=[np.number])
            data = concat([ranked, others], axis=1)
            
        train_y, train_x = self.get_lm_y_x(self._y_key, data[:self._split_date])
        all_y, all_x = self.get_lm_y_x(self._y_key, data)

        self._data_len = len(data)
        self._obj = self._constructor(train_y, train_x)
        self._lm = self._obj.fit()
        self._lm_x = all_x
        self._lm_y = all_y
        
    def get_analysis_results(self):
        xname = self._to_analyze.drop(self._y_key, axis=1).columns.tolist()
        self._summary = self._lm.summary(yname=self._y_key, xname=xname)
        return(self._summary)
        
    def print_analysis_results(self, print_coefs=True):
        """Prints results of analysis.
        
        print_coefs: unused.
        
        """
        print(self.get_analysis_results())
        return(self.get_analysis_results())
            
    def plot_analysis_results(self):
        """Plots predicted versus actual."""
        
        if self._lm_x is None or self._lm_y is None or self._lm is None:
            self.analyze(self._y_key)
        perfect = linear_model.LinearRegression()
        perfect_x = [[y] for y in self._lm_y]
        perfect.fit(perfect_x, self._lm_y)
        
        splt = make_subplot()
        splt.scatter(self._lm.predict(self._lm_x), self._lm_y, color='black')
        splt.plot(perfect.predict(perfect_x), self._lm_y, color='blue')
        
        splt.set_xlabel("Predictions")
        splt.set_ylabel("Actuals")
    
    def compute_model_positions(self, calc_position_size):
        """Computes model positions for each date.
        
        calc_position_size: method to compute position sizes.
        
        """
        predictions = DataFrame(self._lm.predict(self._lm_x))
        predictions.columns = [self.pred_col_name]
        predictions.set_index(self._to_analyze.index, inplace=True)
        
        positions = predictions.groupby(axis=0, level = predictions.index.names.index('Date'))
        positions = positions[self.pred_col_name].apply(calc_position_size)
        positions.columns = [self.pos_col_name]
        combined_df = concat([predictions, positions], axis=1)
        return(combined_df)