#!/usr/bin/env python

"""
Provides deleted code for reference purposes.
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

from DFAnalyzer import DFAnalyzer, median, sign, read_csv
from shortcuts import transform_percentage, transform_reduce_kurtosis, transform_reduce_skewness

df = read_csv('consolidated_wb_data.csv')
labels = ['Date', 'Country']
to_drop =   ['Official exchange rate (LCU per US$, end period)',
             #'Official exchange rate (LCU per US$, period average)',
            'Percent change in Official exchange rate (LCU per US$, period average)',
            'Ease of doing business index (1=most business-friendly regulations)',
            'London Interbank Offered 3-month rates (LIBOR)',
            'London Interbank Offered 6-month rates (LIBOR)',
            'Mainland',
            'Paying taxes (rank)',
            'Protecting investors (rank)']
            
analyzer = DFAnalyzer(df, labels, *to_drop)
y_name = 'Percent change in Official exchange rate (LCU per US$, end period)'
analyzer.analyze(y_name)

#analyzer.load_model(y_name, analyzer.model_path)

"""             
ltransform_args =   [('lambda x,y: transform_reduce_kurtosis(x/y, -1.0)', 'Change in Inventories, constant US$, millions', 'GDP (constant 2000 US$)'),
                     ('log', 'Workers\' remittances, receipts (% of GDP)'),
                     ('log', 'Trade (% of GDP)'),
                     ('log', 'GDP (constant 2000 US$)'),
                     ('log', 'Population, total'), #new coming up
                     ('lambda x: transform_reduce_skewness(x, -1.0)', 'Total tax rate (% of commercial profits)'),
                     ('lambda x: transform_reduce_skewness(x, -1.0)', 'Total debt service (% of GDP)'),
                     ('lambda x: transform_reduce_skewness(x, -1.0)', 'Terms of Trade'),
                     ('lambda x: transform_reduce_skewness(x, -1.0)', 'Risk premium on lending (prime rate minus treasury bill rate, %)'),
                     ('lambda x: transform_reduce_kurtosis(x, 0.5)', 'Return on equity (%)'),
                     ('lambda x: transform_reduce_kurtosis(x, 0.5)', 'Return on assets (%)'),
                     ('lambda x: transform_reduce_kurtosis(x, 0.5)', 'Real interest rate (%)'),
                     ('lambda x: transform_reduce_skewness(x, -0.5)', 'Real Effective Exchange Rate'),
                     ('lambda x: transform_reduce_skewness(x, -0.5)', 'Population in urban agglomerations of more than 1 million (% of total population)'),
                     ('lambda x: transform_reduce_kurtosis(x, 0.5)', 'Population growth (annual %)')]

y_transform_args = (transform_percentage, 'Percent change in Official exchange rate (LCU per US$, end period)')
"""


#analyzer.add_transformation(*y_transform_args, y_key=y_transform_args[1], name=analyzer.compute_name(*y_transform_args), whole_list=True)
#analyzer.make_transformations(ltransform_args)
#analyzer.make_univariate_plots(plot_type=['boxplot', 'probplot'])

#analyzer.compute_name(*y_transform_args)
#outliers = analyzer.get_outliers(y_name)
#analyzer.make_univariate_plot(y_name, plot_type=['boxplot', 'probplot'])

#analyzer.analyze(y_name, normals=True)
#analyzer.print_regression_results(print_coefs=False)
#analyzer.plot_regression_results()


# -*- coding: utf-8 -*-

from pandas import read_excel, concat, DataFrame, read_csv
import Quandl as qd

class FXData:
    
    def __init__(self, load_codes = False, redownload=False):
        if load_codes:
            self.wb_iso_codes = self.load_wb_iso_codes()
    
            self.wb_indicators = self.load_wb_indicators()
            self.wb_qd_codes = self.load_wb_qd_codes()
    
            self.cftc_contracts = self.load_cftc_contracts()
            self.cftc_indicators = self.load_cftc_indicators()
            self.cftc_qd_codes = self.load_cftc_qd_codes()
        
            self.oecd_qd_codes = self.load_oecd_qd_codes()
            
        if redownload:
            self.download_wb_data()
            self.download_cftc_data()
            self.download_oecd_data()
            
        self.consolidated_wb_data = self.consolidate_wb_data()
        self.consolidated_cftc_data = self.consolidate_cftc_data()
        self.consolidated_oecd_data = self.consolidate_oecd_data()
    
    def load_wb_iso_codes(self):
        df = read_excel('iso_codes.xls')
        return dict(zip(df['Country'], df['World Bank Code']))
        
    def load_wb_indicators(self):
        df = read_excel('wb_indicator_codes.xls')
        return dict(zip(df['Indicator Name'], df['Code']))
        
    def load_wb_all_qd_codes(self):
        #df = read_excel('all_world_bank_codes.xls')
        df = read_csv('all_world_bank_codes.csv', encoding = "ISO-8859-1")
        return df[df.columns[0]].tolist()
    
    def load_wb_qd_codes(self):
        wb_qd_codes = dict()
        all_wb_qd_codes = self.load_wb_all_qd_codes()
        for country, country_code in self.wb_iso_codes.items():
            for indicator, indicator_code in self.wb_indicators.items():
                key = '%s: %s' % (country, indicator)
                value = 'WORLDBANK/%s_%s' % (country_code, indicator_code)
                if value in all_wb_qd_codes:
                    wb_qd_codes[key] = value
        
        return wb_qd_codes
        
    def load_cftc_contracts(self):
        df = read_excel('cftc_contracts.xls')
        return dict(zip(df['Name'], df['Symbol']))
    
    def load_cftc_indicators(self):
        df = read_excel('cftc_indicators.xls')
        return dict(zip(df['Name'], df['Code']))
        
    def load_all_cftc_qd_codes(self):
        df = read_csv('all_cftc_codes.csv')
        return df[df.columns[0]].tolist()

    def load_cftc_qd_codes(self):
        cftc_qd_codes = dict()
        all_cftc_codes = self.load_all_cftc_qd_codes()
        for contract_name, contract_code in self.cftc_contracts.items():
            for indicator_name, indicator_code in self.cftc_indicators.items():
                key = '%s: %s' % (contract_name, indicator_name)
                value = 'CFTC/%s_%s' % (contract_code, indicator_code)
                if value in all_cftc_codes:
                    cftc_qd_codes[key] = value
        return cftc_qd_codes
        
    def load_all_oecd_qd_codes(self):
        df = read_csv('all_oecd_codes.csv')
        return df[df.columns[0]].tolist()
    
    def load_oecd_qd_codes(self):
        # The OECD database is poorly designed with no documentation.
        #hourly earnings manufacturing 
        oecd_qd_codes = dict()      
        all_oecd_codes = self.load_all_oecd_qd_codes()
        ind_name, ind_code = "Composite Leading Index", "OECD/MEI_CLI_LOLITOAA"
        ends = dict(zip(["Monthly", "Quarterly", "Annually", ""], ["_M", "_Q", "_A", ""]))
        for period_name, period_code in ends.items():
            for country, country_code in self.wb_iso_codes.items():
                key = "%s: %s, %s" % (country, ind_name, period_name)
                value = "%s_%s%s" % (ind_code, country_code, period_code)
                
                if value in all_oecd_codes:
                    oecd_qd_codes[key] = value
        return oecd_qd_codes
        
    def download_wb_data(self):
        names = list(self.wb_qd_codes.keys())
        codes = list(self.wb_qd_codes.values())
        
        left_bound = 0
        right_bound = 500
        codes_len = codes.__len__()
        
        downloads = []
        
        while right_bound < codes_len:
            dd = qd.get(codes[left_bound:right_bound], authtoken='LJ3oEd-suo-8p4o4542_')
            dd.columns = names[left_bound:right_bound]
            downloads.append(dd)
            left_bound = left_bound + 500
            right_bound = right_bound + 500
            print("A success")
        else:
            dd = qd.get(codes[left_bound:], authtoken='LJ3oEd-suo-8p4o4542_')
            dd.columns = names[left_bound:]
            downloads.append(dd)
            print("Final success!")
        
        
        all_downloaded_data = concat(downloads, axis=1)
        all_downloaded_data.to_csv('wb_data.csv')
        
    def cleanup_cftc_data(self, df):
        #Ex: CFTC.SI_FO_ALL - Producer/Merchant/Processor/User Shorts
        df = df.dropna(axis=1,how='all')
        ncolnames = []
        for name in df.columns:
            rm_cftc = name.split('.')[1]
            sym = rm_cftc.split('_')[0]
            ind = rm_cftc.split(' - ')[-1]
            
            sym_name = list(self.cftc_contracts.keys())[list(self.cftc_contracts.values()).index(sym)]
            ncolnames.append('%s - %s' % (sym_name, ind))
            
        df.columns = ncolnames
        return df
        
    def download_cftc_data(self):
        codes = list(self.cftc_qd_codes.values())
        all_downloaded_data = qd.get(codes, authtoken='LJ3oEd-suo-8p4o4542_')
        
        to_export = self.cleanup_cftc_data(all_downloaded_data)
        to_export.to_csv('cftc_data.csv')
        
    def download_oecd_data(self):
        names = list(self.oecd_qd_codes.keys())
        codes = list(self.oecd_qd_codes.values())
        all_downloaded_data = qd.get(codes, authtoken='LJ3oEd-suo-8p4o4542_')
        all_downloaded_data.columns = names
        all_downloaded_data.to_csv('oecd_data.csv')
        
    def generic_consolidate_data(self, path, english_to_symbol_indicator, indicator_handler):
        data = read_csv(path, index_col=0)
        cols = list(data.columns)
        indices = list(data.index)
        
        vals = {}
        ldata = data.values.tolist()
        
        for col_idx, col in enumerate(cols):
            symbol, indicator = english_to_symbol_indicator(col)
            for row_idx, date in enumerate(indices[:-1]):
                key = {"Country": symbol, "Date": date}
                
                to_update = {indicator: ldata[row_idx][col_idx]}
                to_update.update(indicator_handler(indicator, ldata[row_idx][col_idx], ldata[row_idx+1][col_idx]))
                frozen_key = frozenset(key.items())
                if frozen_key in vals:
                    vals[frozen_key].update(to_update)
                else:
                    vals[frozen_key] = to_update
        
        data_as_list_of_dicts = []
        for country_date, indicators in vals.items():
            to_append = {}
            to_append.update(country_date)
            to_append.update(indicators)
            data_as_list_of_dicts.append(to_append)
            
        return DataFrame(data_as_list_of_dicts)
        
    def _wb_english_to_symbol_indicator(self, english):
        sp = english.split(': ')
        symbol = sp[0]
        ind = sp[1]
        return symbol, ind
        
    def _wb_indicator_handler(self, indicator, current_val, next_val):
        to_handle = ["Official exchange rate (LCU per US$, period average)",
                     "Official exchange rate (LCU per US$, end period)",
                     "Export price index (goods and services, 2000=100)",
                     "Import price index (goods and services 2000=100)"]
        if indicator in to_handle:
            percent_change = ((next_val - current_val) / current_val)* 100
            return {"Percent change in %s" % indicator: percent_change}
        else:
            return {}
        
    def consolidate_wb_data(self):
        res = self.generic_consolidate_data('wb_data.csv', self._wb_english_to_symbol_indicator, self._wb_indicator_handler)   
        res.to_csv('consolidated_wb_data.csv')
        return res

    def _cftc_english_to_symbol_indicator(self, english):
        sp = english.split(' - ')
        symbol = sp[0]
        ind = sp[1]
        return symbol, ind
        
    def _cftc_indicator_handler(self, indicator, current_val, next_val):
        return {}
    
    def consolidate_cftc_data(self):
        res =  self.generic_consolidate_data('cftc_data.csv', self._cftc_english_to_symbol_indicator, self._cftc_indicator_handler)
        res.to_csv('consolidated_cftc_data.csv')
        return res
        
    def _oecd_english_to_symbol_indicator(self, english):
        return self._wb_english_to_symbol_indicator(english) # same as wb coding
        
    def _oecd_indicator_handler(self, indicator, current_val, next_val):
        return {}
        
    def consolidate_oecd_data(self):
        res = self.generic_consolidate_data('oecd_data.csv', self._oecd_english_to_symbol_indicator, self._oecd_indicator_handler)
        res.to_csv('consolidated_oecd_data.csv')
        return res
        
        
 def process(self, path, compute_names, english_to_symbol_indicator, indicator_handler, symbol_name, date_name='Date', resample_method='A'):
        data = self._downloaded_data
        data.dropna(axis=1, how='all', inplace=True)
        data.set_index(date_name, drop=True, inplace=True)
        data.index = to_datetime(data.index)
        if resample_method is not None:
            data = data.resample(resample_method).pad()
        
        data.columns = compute_names(data.columns)
        cols = list(data.columns)
        indices = list(data.index)
        
        vals = {}
        ldata = data.values.tolist()
        
        for col_idx, col in enumerate(cols):
            symbol, indicator = english_to_symbol_indicator(col)
            for row_idx, date in enumerate(indices[1:-1]):
                key = {symbol_name: symbol, date_name: date}
                
                to_update = {indicator: ldata[row_idx][col_idx]}
                to_update.update(indicator_handler(indicator, ldata[row_idx-1][col_idx], ldata[row_idx][col_idx], ldata[row_idx+1][col_idx]))
                frozen_key = frozenset(key.items())
                if frozen_key in vals:
                    vals[frozen_key].update(to_update)
                else:
                    vals[frozen_key] = to_update
        
        data_as_list_of_dicts = []
        for country_date, indicators in vals.items():
            to_append = {}
            to_append.update(country_date)
            to_append.update(indicators)
            data_as_list_of_dicts.append(to_append)
            
        self._processed_data = DataFrame(data_as_list_of_dicts)
        self._processed_data.to_csv(path)
        
        
def wb_indicator_handler(indicator, prev_val, current_val, next_val):
    res = {}
    to_handle = ["Official exchange rate (LCU per US$, period average)",
                 "Official exchange rate (LCU per US$, end period)",
                 "Export price index (goods and services, 2000=100)",
                 "Import price index (goods and services 2000=100)",
                 "Average precipitation in depth (mm per year)",
                 "Bank capital to assets ratio (%)",
                 "Global Competitiveness Index (GCI)",
                 "Real interest rate (%)",
                 "Return on assets (%)",
                 "Return on equity (%)"]
    if indicator in to_handle:
        key = "Percent change in %s" % indicator
        
        if isnan(current_val) or isnan(next_val) or current_val==0.0 or next_val==0.0:
            res.update({key: float('nan')})
        else:
            percent_change = ((next_val - current_val) / current_val)* 100
            res.update({key: percent_change})
            
        key = "Previous " + key
        
        if isnan(prev_val) or isnan(current_val) or prev_val==0.0 or current_val==0.0:
            res.update({key: float('nan')})
        else:
            percent_change = ((current_val - prev_val) / prev_val)* 100
            res.update({key: percent_change})
            
    return(res)
    
def get_fx_info():
    fx_info = {}
    fx_info["authtoken"] = sam_authtoken
    fx_info["main_db_name"] = "World Bank"
    
    iso_codes = DBSymbol('iso_codes.xls', 'Country', 'World Bank Code', read_excel)
    wb_indicators = DBSymbol('wb_indicator_codes.xls', 'Indicator Name', 'Code', read_excel)
    
    cftc_contracts = DBSymbol('cftc_contracts.xls', 'Name', 'Symbol', read_excel)
    cftc_indicators = DBSymbol('cftc_indicators.xls', 'Name', 'Code', read_excel)
    
    uifs_codes = DBSymbol('uifs_codes.xls', 'COUNTRY or AREA', 'CODE', read_excel)
    uifs_indicators = DBSymbol('uifs_indicators.xls', 'Name', 'Code', read_excel)
    
    wb_info = {}
    wb_info["symbols"] = [iso_codes, wb_indicators]
    wb_info["downloaded_data"] = {"path": "wb_data.csv"}
    #wb_info["all_codes"] = {"path": 'all_world_bank_codes.csv', "loader": read_csv_iso}
    wb_info["create_downloader"] = qd_downloader_func(fx_info)
    wb_info["code_builder"] = wb_code_builder
    wb_info["name_builder"] = wb_name_builder
    wb_info["english_to_symbol_indicator"] = wb_english_to_symbol_indicator
    wb_info["indicator_handler"] = wb_indicator_handler
    wb_info["download_and_save"] = {"path": "wb_data.csv"}
    wb_info["process"] = {"path": "wb_processed_data.csv", "compute_names": wb_compute_names, "load": True}
    wb_info["symbol_name"] = 'Country'
    wb_info["date_name"] = 'Date'
    
    cftc_info = {}
    cftc_info["symbols"] = [cftc_contracts, cftc_indicators]
    cftc_info["downloaded_data"] = {"path": "cftc_data.csv"}
    cftc_info["create_downloader"] = qd_downloader_func(fx_info)
    cftc_info["code_builder"] = cftc_code_builder
    cftc_info["name_builder"] = cftc_name_builder
    cftc_info["english_to_symbol_indicator"] = cftc_english_to_symbol_indicator
    cftc_info["indicator_handler"] = cftc_indicator_handler
    cftc_info["download_and_save"] = {"path": "cftc_data.csv"}
    cftc_info["process"] = {"path": "cftc_processed_data.csv", "compute_names": cftc_compute_names, "load": True}
    cftc_info["symbol_name"] = 'Country'
    cftc_info["date_name"] = 'Date'
    
    oecd_info = {}
    #oecd_info["all_codes"] = {"path": 'all_oecd_codes.csv'}
    oecd_info["create_downloader"] = qd_downloader_func(fx_info)
    oecd_info["downloaded_data"] = {"path": "oecd_data.csv"}
    oecd_info["compute_wanted_codes"] = {"data": load_oecd_qd_codes()}
    oecd_info["english_to_symbol_indicator"] = oecd_english_to_symbol_indicator
    oecd_info["indicator_handler"] = oecd_indicator_handler
    oecd_info["download_and_save"] = {"path": "oecd_data.csv"}
    oecd_info["process"] = {"path": "oecd_processed_data.csv", "compute_names": oecd_compute_names, "load": True}
    oecd_info['symbol_name'] = 'Country'
    oecd_info['date_name'] = 'Date'
    
    currfx_info = {}
    currfx_info["create_downloader"] = qd_downloader_func(fx_info)
    currfx_info["compute_wanted_codes"] = {"data": load_currfx_qd_codes()}
    currfx_info["downloaded_data"] = {"path": "currfx_data.csv"}
    currfx_info["download_and_save"] = {"path": "currfx_data.csv"}
    currfx_info["process"] = {"path": "currfx_processed_data.csv", "compute_names": currfx_compute_names, "load": True}
    currfx_info["english_to_symbol_indicator"] = currfx_english_to_symbol_indicator
    currfx_info["indicator_handler"] = currfx_indicator_handler
    currfx_info['symbol_name'] = 'Country'
    currfx_info['date_name'] = 'Date'
    
    uifs_info = {} 
    uifs_info["downloaded_data"] = {"path": "uifs_data.csv"}
    uifs_info["create_downloader"] = qd_downloader_func(fx_info)
    uifs_info["symbols"] = [uifs_codes, uifs_indicators]
    uifs_info["code_builder"] = uifs_code_builder
    uifs_info["name_builder"] = uifs_name_builder
    uifs_info["english_to_symbol_indicator"] = uifs_english_to_symbol_indicator
    uifs_info["indicator_handler"] = uifs_indicator_handler
    uifs_info["download_and_save"] = {"path": "uifs_data.csv"}
    uifs_info["process"] = {"path": "uifs_processed_data.csv", "compute_names": uifs_compute_names, "load": True}
    uifs_info['symbol_name'] = 'Country'
    uifs_info['date_name'] = 'Date'
    
    db_info = {}
    db_info["World Bank"] = wb_info
    db_info["OECD"] = oecd_info
    db_info["CFTC"] = cftc_info
    db_info["CURRFX"] = currfx_info
    #db_info["UIFS"] = uifs_info The data for exchange rates is difficult to interpret.
    
    fx_info["dbs"] = db_info
    fx_info["combined_df"] = {}
    fx_info["combined_df"]["path"] = 'combined_fx_data.csv'
    fx_info["combined_df"]["labels"] = ['Date', 'Country']
    fx_info["combined_df"]["to_drop"] = ['Official exchange rate (LCU per US$, end period)',
                    'Official exchange rate (LCU per US$, period average)',
                    'Percent change in Official exchange rate (LCU per US$, period average)',
                    'Ease of doing business index (1=most business-friendly regulations)',
                    'London Interbank Offered 3-month rates (LIBOR)',
                    'London Interbank Offered 6-month rates (LIBOR)',
                    'Mainland',
                    'Paying taxes (rank)',
                    'Protecting investors (rank)',
                    'CURRFX Low (est)',
                    'CURRFX High (est)']
    fx_info["combined_df"]["names"] = ["DB", "Indicator"]
    fx_info["combined_df"]["transformer"] = combined_df_transformer
    fx_info["create_analyzer"] = {"func": reg_create_func(fx_info), "path": "fx_model.pickle", "load": True}
    fx_info["y_key"] = ('CURRFX', 'Future Percent change in CURRFX Rate') # Shouldn't have to do this. Maybe change in later version
    
    return(fx_info)
    
# This requires whole_list=True
def transform_percentage(x):
    """Transforms proportions into 
    multiples = [0.01*(el[0]+100) for el in x] # multiple. #Now think of multiple = Ae^rt.
    unskewed = transform_reduce_skewness(multiples, -2.0)
    unkurt = transform_reduce_kurtosis(unskewed, 0.5)
    return unkurt
    """
    
    
#def make_SF0_col_handler():
#    codes = load_SF0_qd_codes()
#    codes.set_index('Code', inplace=True)
#    codes.sort_index(inplace=True)
#    def res(col_name):
#        qd_code = 'SF0/%s' % col_name
#        try:
#            name = codes.loc[qd_code]['Name']
#        except:
#            name = "%s: %s" % (qd_code, "Missing")
#        return(name)
#    return(res)
    
    

    """
    equity_info.dbs.INDUSTRY. \
        set_path('download_and_save', 'SF0-tickers.csv'). \
        downloader(creator=meta_loader_creator).set(no_compute_codes=True). \
        set(english_to_symbol_indicator=default_english_to_symbol_indicator). \
        set(indicator_handler=make_default_indicator_handler([], [])). \
        set_path('process', load=True, path='SF0-tickers.csv'). \
        set(symbol_name="Security", date_name="Date") 
    """
    
    #set_path('downloaded_data', 'SF0-tickers.csv'). \
    #'INDUSTRY-processed-data.csv',
                # compute_names=make_default_compute_names([], identity),
                # load=False, idx_to_datetime=identity, resample_method=None). \
    
    #Doing this differently: res.add_transformation(identity, ('INDUSTRY', 'Sector'), name=('CALC', 'Sector'), drop_old=False)        
        
        #res.add_transformation(log, ('SF0', 'Revenues (USD)'), name=('CALC', 'size'), drop_old=False)
        #res.add_transformation(identity, ('SF0', 'Current Ratio'), name=('CALC', 'Current Ratio'), drop_old=False)
        #res.add_transformation(identity, ('SF0', 'Debt to Equity Ratio'), name=('CALC', 'Debt to Equity Ratio'), drop_old=False)        
        #res.add_transformation(smart_divide, ('SF0', 'Gross Profit'), ('SF0', 'Revenues (USD)'), name=('CALC', 'Gross Margin'), drop_old=False)