# Import Modules
from abc import ABC, abstractmethod

class AttackClass(ABC):
    def __init__(self, model, dataset_struct=None, dataset_stats=None, params=None):
        self.model = model
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.params = params

    @abstractmethod
    def create_keras_classifier(self):
        pass
    
    @abstractmethod
    def perform_attack(self):
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
