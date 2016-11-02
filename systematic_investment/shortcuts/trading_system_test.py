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

def test_data_processing(info):
    """Tests data processing functionality.
    
    info: an Info object with settings information.
    
    """
    from systematic_investment.data import DataLoader
    
    dl = DataLoader(info.attr_dict())
    combiner = dl.load()
    return(combiner)
    
import matplotlib.pyplot as plt
    
def test_models(info, action, *model_classes):
    """Tests models.
    
    info: an Info object with settings.
    
    action: what to do with the model.
    
    model_classes: constructors of models from info.
    
    """
    res = []
    for model_class in model_classes:
        model = model_class(info)
        res.append(action(model))
    return(res)
        