# Utils
import json
import cv2

from datetime import datetime

# System
import os

# Adversarial Robustness Toolkit - Keras Classifier
from art.estimators.classification import KerasClassifier

###################################################################################################

# Abstract Class
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
            model=model,                    # The Keras model
            use_logits=False,               # Use logit outputs instead of probabilities (default: False)
            channels_first=False,           # Whether channels are the first dimension in the input data (default: False)
            clip_values=(0, 1),             # Range of valid input values (default: (0,1))
            preprocessing_defences=None,    # Defenses for pre-processing the data (default: None)
            postprocessing_defences=None,   # Defenses for post-processing the results (default: None)
            preprocessing=(0, 1),           # Preprocessing clip values (default: (0,1))
            input_layer=0,                  # Input layer of the model (default: 0)
            output_layer=-1                 # Output layer of the model (default: -1)
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
    
    def save_images(self, tag = "AttackClass", images = [], save_path = "../storage/results", uid = datetime.now().strftime("%Y%m%d%H%M%S%f")):
        # Create all directory and file tree
        dirname = f"{tag}-summary-{uid}"
        
        dir_path = os.path.join(save_path, dirname)
        
        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Save proof images
        for i in range(min(len(images), 3)):
            cv2.imwrite(os.path.join(dir_path, f'{tag}_image{i+1}.png'), images[i])
            
    def save_summary(self, tag = "AttackClass", result = {}, images = None, save_path = "../storage/results", uid = datetime.now().strftime("%Y%m%d%H%M%S%f")):
        # Create all directory and file tree
        filename = f"{tag}-summary-{uid}.json"
        dirname = f"{tag}-summary-{uid}"
        
        dir_path = os.path.join(save_path, dirname)
        
        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Save some sample images
        if images:
            self.save_images(tag, images, save_path, uid)
        
        # Save the json summary
        with open(os.path.join(dir_path, filename), 'w') as file:
            json.dump(result, file, indent=4)

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
