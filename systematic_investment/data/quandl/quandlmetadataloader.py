# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 15:33:13 2016

@author: davidadelberg
"""

from systematic_investment.data.dbloader import DBLoader
from systematic_investment.shortcuts import read_csv_iso

class QuandlMetaDataLoader(DBLoader):
    
    def __init__(self, wanted_columns, path, loader=read_csv_iso, *args, **kwargs):
        super(DBLoader, self).__init__(*args, **kwargs)
        self._wanted_columns = wanted_columns
        self._all_data = loader(path)
        self.load_wanted_codes(path, loader)
        
    def download_and_save(self, path):
        selected_data = self._all_data[self._wanted_columns]
        selected_data.to_csv(path)
        self._downloaded_data = selected_data
        