#Import Modules
from art.attacks.extraction import CopycatCNN
from art.estimators.classification import KerasClassifier

class CopycatCNN:
    def __init__(self, dataset_struct, dataset_stats, model, params):
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.model_original = model
        self.params = params
    