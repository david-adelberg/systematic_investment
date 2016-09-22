#!/usr/bin/env python

"""
In progress

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
__status__ = "Prototype"

from systematic_investment.data.dbsymbol import DBSymbol
from systematic_investment.shortcuts import qd_downloader_func, reg_create_func
    
class Info(object):
    def __init__(self, data_dir='/', up=None, **kwargs):
        """Creates an Info object.
        
        data_dir: data is stored in this relative path.
        
        up: the parent Info object.
        
        kwargs: unused.
        
        """
        self._up=up
        self._data_dir=data_dir
        
        for key, val in kwargs.items():
            self.__setattr__(key, val)
            
    def attr_dict(self):
        """Gets nested dict of user-supplied data."""
        
        base_keys = set(Info().__dict__.keys())
        self_keys = set(self.__dict__.keys())
        res = {}
        for key in self_keys.difference(base_keys):
            val = self.__dict__[key]
            try:
                res[key] = val.attr_dict()
            except AttributeError:
                res[key] = val
        
        return(res)
        
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
        
    def info(self, name, **kwargs):
        """Sets self.name to be an Info object with parent self.
        
        name: name of the field created.
        
        kwargs: passed to Info.
        
        """
        i = Info(up=self, **kwargs)
        self.__setattr__(name, i)
        
        return(i)
        
    def up(self):
        """Gets parent Info object."""
        return(self._up)
        
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
        
    def set(self, **kwargs):
        """Adds fields to Info.
        
        kwargs: Each key, value pair corresponds to a new field in the object.
        
        """
        for key, val in kwargs.items():
            self.__setattr__(key, val)
        
        return(self)
        
    def top(self):
        """Gets the root Info object."""
        if self.up() is None:
            return(self)
        else:
            return(self.up().top())
        
    def __getattr__(self, name):
        """Creates a new field name set to a child Info object.
        
        name: the name of the field to create.
        """
        
        self.__setattr__(name, Info(data_dir=self._data_dir, up=self))
        return(self.__dict__[name])

