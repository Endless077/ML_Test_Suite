#Import Modules
from art.attacks.inference.model_inversion import MIFace
from art.estimators.classification import KerasClassifier

class MIFace:
    def __init__(self, dataset_struct, dataset_stats, params):
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.model = model
        self.params = params