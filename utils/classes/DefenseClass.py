# Utils
import numpy as np
import tensorflow as tf
from art.estimators.classification import KerasClassifier

# Import Modules
from abc import ABC, abstractmethod

class DefenseClass(ABC):
    def __init__(self, vulnerable_model=None, robust_model=None, dataset_struct=None, dataset_stats=None, params=None):
        self.vulnerable_model = vulnerable_model
        self.robust_model = robust_model
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.params = params

    def create_keras_classifier(self, model, preprocessing_defences=None, postprocessing_defences=None):
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        classifier = KerasClassifier(
            model=model,                                        # The Keras model
            use_logits=False,                                   # Use logit outputs instead of probabilities (default: False)
            channel_index=-1,                                   # Index of the channel axis in the input data (default: -1)
            preprocessing_defences=preprocessing_defences,      # Defenses for pre-processing the data (default: None)
            postprocessing_defences=postprocessing_defences,    # Defenses for post-processing the results (default: None)
            input_layer=0,                                      # Input layer of the model (default: 0)
            output_layer=-1,                                    # Output layer of the model (default: -1)
            channels_first=False,                               # Whether channels are the first dimension in the input data (default: False)
            clip_values=(0, 1)                                  # Range of valid input values (default: (0,1))
            )
        
        return classifier
    
    @abstractmethod
    def perform_defense(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def plotting_stats(self):
        pass

    @abstractmethod
    def result(self):
        pass
    
class DetectorDefense(DefenseClass):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)
    
    @abstractmethod
    def perform_defense(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass
    
    @abstractmethod
    def plotting_stats(self):
        pass
    
    @abstractmethod
    def result(self):
        pass
    
class PostprocessorDefense(DefenseClass):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)

    @abstractmethod
    def perform_defense(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass
    
    @abstractmethod
    def plotting_stats(self):
        pass

    @abstractmethod
    def result(self):
        pass
    
class PreprocessorDefense(DefenseClass):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)
    
    @abstractmethod
    def perform_defense(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def plotting_stats(self):
        pass

    @abstractmethod
    def result(self):
        pass
    
class TrainerDefense(DefenseClass):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)
    
    @abstractmethod
    def perform_defense(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def plotting_stats(self):
        pass
    
    @abstractmethod
    def result(self):
        pass
     
class TransformerDefense(DefenseClass):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)
        
    @abstractmethod
    def perform_defense(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def plotting_stats(self):
        pass

    @abstractmethod
    def result(self):
        pass
