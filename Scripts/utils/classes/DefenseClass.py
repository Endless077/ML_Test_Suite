# Import Modules
from abc import ABC, abstractmethod

class DefenseClass(ABC):
    def __init__(self, vulnerable_model=None, robust_model=None, dataset_struct=None, dataset_stats=None, params=None):
        self.vulnerable_model = vulnerable_model
        self.robust_model = robust_model
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.params = params

    @abstractmethod
    def create_keras_classifier(self):
        pass
    
    @abstractmethod
    def perform_defense(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass
    
    @abstractmethod
    def print_stats(self):
        pass

    @abstractmethod
    def plotting_stats(self):
        pass
