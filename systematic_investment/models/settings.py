#!/usr/bin/env python

"""
Provides Info, a dynamic class for easy declaration of settings.

Info implements a fluent interface for adding settings to the object.
Info implements methods to add a symbol, to add a path, and to set values,
and to convert to a nested dict.
Additionally, Info fields are automatically assigned type Info unless assigned
a value by the user, so Info().dbs.DB.set_path(...), for example, is possible.
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

from .DBSymbol import DBSymbol
from .shortcuts import qd_downloader_func, reg_create_func, data_dir, identity
from .InfoNew import Info
    
class Settings(Info):
    def __init__(self, data_dir='/', up=None, **kwargs):
        """Creates an Info object.
        
        data_dir: data is stored in this relative path.
        
        up: the parent Info object.
        
        kwargs: unused.
        
        """
        super(Settings, self).__init__(**kwargs)
        
        self._up=up
        self._data_dir=data_dir
        self._attr_handler = lambda name: Settings(data_dir=self._data_dir, up=self)
        
    def symbol(self, path, *args, **kwargs):
        """Adds a symbol to the object.
        
        path: symbol path.
        
        args: passed to DBSymbol.
        
        kwargs: passed to DBSymbol.
        
        """
        sym = DBSymbol(self._fix_path(path), *args, **kwargs)

        try:
            self.symbols.append(sym)
        except TypeError:
            self.symbols = [sym]
        
        return(self)
        
    def _fix_path(self, path):
        """Gets the path name after prepending self._data_dir."""
        return(self._data_dir+path)
        
    def set_path(self, name, path, **kwargs):
        """Adds a new path attribute with name name.
        
        name: name of the attribute.
        
        path: path string.
        
        kwargs: passed to Info.set().
        
        """
        self.__getattr__(name).path=self._fix_path(path)
        self.__dict__[name].set(**kwargs)
        return(self)
        
    def downloader(self, creator=qd_downloader_func):
        """Adds a downloader to self.
        
        creator: function to create a downloader.
        
        """
        self.create_downloader = creator(self)
        return(self)
        
    def create_analyzer(self, creator=reg_create_func):
        """Adds an analyzer to self.
        
        creator: function to create the analyzer.
        
        """
        self.analyzer.create = creator(self.top())
        return(self)
      
    def _default_attr_handler(self, name):
        return(Settings(data_dir=self._data_dir, up=self))
        
    def make_default_db(self, name):
        if 'main_db_name' not in self.top().__dict__:
            self.top().main_db_name=name
        
        self.__getattr__(name).set(
            code_builder=make_default_code_builder(name),
            name_builder=default_name_builder,
            english_to_symbol_indicator=default_english_to_symbol_indicator,
            indicator_handler=make_default_indicator_handler([],[])). \
            set_path('download_and_save', name+'_data.csv'). \
            set_path('process', name+"_processed_data.csv",
                     compute_names=make_default_compute_names(['Date'], identity)). \
            set(symbol_name='Security', date_name='Date')
        
        return(self.__getattr__(name))                         
        
    def _db_attr_handler(self, name):
        res = self._default_attr_handler(name)
        res._attr_handler = self.make_default_db
        return(res)
        
    @staticmethod
    def create(name):
        res = Settings(data_dir=data_dir)
        res.dbs._attr_handler =  res.dbs._db_attr_handler
        res.set_path('combined_df', 'combined_%s_data.csv' % name,
                     labels=['Date', 'Security'], to_drop=[], transformer=identity,
                     names=['DB', 'Indicator']). \
            set_path('analyzer', name+'_analyzer.pickle', load=False). \
            create_analyzer()
            
        return(res)
