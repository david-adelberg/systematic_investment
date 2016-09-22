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
from pandas import read_excel

data_dir='data/'

def read_csv_iso(path):
    """Read csv file with ISO-8859-1 encoding."""
    
    return read_csv(path, encoding = "ISO-8859-1")
    
def fix_read_excel(path, **kwargs):
    return(read_excel(data_dir+path, **kwargs))
    
def default_indicator_loader(path, loader=fix_read_excel):
    return(loader(path))