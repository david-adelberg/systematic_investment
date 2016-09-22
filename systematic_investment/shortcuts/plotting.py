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

import matplotlib.pyplot as plt
from pandas.tools.plotting import boxplot_frame_groupby
        
def make_subplot():
    """Utility method to make a subplot."""
    return(plt.figure().add_subplot(1,1,1))
    
def plot_returns(returns, live_date=None):
    plt.figure()
    ax = make_subplot()
    if live_date is not None:
        returns[:live_date].plot(ax=ax, label="train")
        returns[live_date:].plot(ax=ax, label="test")
    else:
        returns.plot(ax=ax, label="all")
        
def make_boxplots(df, by, title):
    make_subplot()
    grouped = df.groupby(axis=0, level=df.index.names.index(by))
    boxplot_frame_groupby(grouped, subplots=False, rot=90, return_type='axes')
    plt.title(title)
    