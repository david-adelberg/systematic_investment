#!/usr/bin/env python

"""
In progress

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

from .DBSymbol import DBSymbol
from .shortcuts import qd_downloader_func, reg_create_func
    
class Info(object):
    def __init__(self, attr_handler = lambda name: Info(), **kwargs):
        """Creates an Info object.
        
        data_dir: data is stored in this relative path.
        
        up: the parent Info object.
        
        kwargs: unused.
        
        """
        
        self._attr_handler = attr_handler
        
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
        
    def up(self):
        """Gets parent Info object."""
        return(self._up)
        
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
        
        self.__setattr__(name, self._attr_handler(name))
        return(self.__dict__[name])

