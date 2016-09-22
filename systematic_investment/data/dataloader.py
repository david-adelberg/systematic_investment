#!/usr/bin/env python

"""
Provides DataLoader, a class to manage the (down)loading, processing, and combining of data.

DataLoader holds a nested dictionary _info that contains settings which guide execution.
The class defines do_downloads, do_processing, and do_combining methods,
as well as a load method that performs loading, processing, and combining
(if instructed to do so by _info.)

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

from .dbcombiner import DBCombiner
from pandas import read_csv

class DataLoader:
    
    def __init__(self, info, *args, **kwargs):
        """Returns new DataLoader object with specificied info.
        
        info: a dict of settings to guide the DataLoader
        
        args: unused
        
        kwargs: unused
        """
        
        self._info = info
    
    def do_downloads(self, verbose=True):
        """(Down)loads all data, according to the settings in self._info.
        
        verbose: Should the method print status information?
        
        """
        res = {}
        for db_name, db_info in self._info["dbs"].items():
            d = db_info["create_downloader"]()
            cwc_kwargs = {}
            
            if "downloaded_data" in db_info.keys():
                if verbose:
                    print("Loading data from %s" % db_name)
                dd_info = db_info["downloaded_data"]
                if "data" in dd_info.keys():
                    d._downloaded_data = dd_info["data"]
                    res[db_name] = d
                    continue
                else:
                    d.load_downloaded_data(**dd_info)
                    res[db_name] = d
                    continue
                    
            elif "all_codes" in db_info.keys():
                ac_info = db_info["all_codes"]
                cwc_kwargs["all_valid_codes"] = d.load_all_codes(**ac_info)
                
            cwc_info = {}
            if "compute_wanted_codes" in db_info.keys():
                cwc_info = db_info["compute_wanted_codes"]
            if "data" in cwc_info.keys():
                d._wanted_codes = cwc_info["data"]
            else:
                if "path" in cwc_info.keys():
                    cwc_kwargs["path"] = cwc_info["path"]
                if "no_compute_codes" not in db_info.keys():
                    d.compute_wanted_codes(db_info["code_builder"], db_info["name_builder"], db_info["symbols"], **cwc_kwargs)
            
            if verbose:
                print("Downloading data from %s" % db_name)
            d.download_and_save(**db_info["download_and_save"])
            res[db_name] = d
            
        return(res)
        
    def do_processing(self, d_dict, verbose=True):
        """Processes data according to settings in self._info.
        
        d_dict: a dict mapping names to DBLoaders.
        
        verbose: Should status information be printed?
        """
        
        res = {}
        for db_name, downloader in d_dict.items():
            db_info = self._info["dbs"][db_name]
            if db_info["process"]["load"]:
                if verbose:
                    print("Loading processed data from %s" % db_name)
                downloader._processed_data = read_csv(db_info["process"]["path"], index_col=[0,1])
            else:
                if verbose:
                    print("Processing data from %s" % db_name)
                
                the_kwargs = {}
                if "idx_to_datetime" in db_info["process"]:
                    the_kwargs["idx_to_datetime"] = db_info["process"]["idx_to_datetime"]
                if "resample_method" in db_info["process"]:
                    the_kwargs["resample_method"] = db_info
                    
                downloader.process(**db_info, **db_info["process"])
                #downloader.process(db_info["process"]["path"], db_info["process"]["compute_names"], db_info["english_to_symbol_indicator"], db_info["indicator_handler"], db_info["symbol_name"], db_info["date_name"], **the_kwargs)
            res[db_name] = downloader
            
        return(res)
        
    def do_combining(self, processed_dfs, min_date='1900-01-01', to_drop = [], verbose=True):
        """Combines processed_dfs according the settings in self._info.
        
        processed_dfs: a dict mapping names to DataFrames
        
        to_drop: a list of columns to drop.
        
        verbose: Should status information be printed?
        
        """
        
        combiner = DBCombiner(processed_dfs)
        return(combiner.combine(to_drop=to_drop, min_date=min_date, combined_names=self._info["combined_df"]["names"], path=self._info["combined_df"]["path"], transformer=self._info["combined_df"]["transformer"], combine_func=self._info["combined_df"]["combine_func"]))
        
    def load(self, verbose=True):
        """Performs loading, processing, and combining according to self._info.
        
        verbose: Should status information be printed?
        
        """
        
        downloads = self.do_downloads(verbose)
        processed = self.do_processing(downloads, verbose)
        dfs = {key: d._processed_data for key, d in processed.items()}
        combiner = self.do_combining(dfs, min_date=self._info["combined_df"]["min_date"], to_drop=self._info["combined_df"]["to_drop"], verbose=verbose)
        return(combiner)