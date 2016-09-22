#!/usr/bin/env python

"""
In progress

Provides utility scripts for the equity trading model.
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

from pandas import read_csv

def split_data_by(df, split_by='Sector'): 
    industry_table = read_csv("data/SF0-tickers.csv")
    security_types = set(df[split_by]).tolist()
    df = df.T
    sec_type_to_cols = {sec_type: [] for sec_type in security_types}
    for fundamentals_row in df:
        ticker = row.name[1]
        ticker_type = industry_table[ticker][split_by]
    
equities_data = read_csv("data/SF0-processed-data.csv")