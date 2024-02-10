# Import Abstract
from abc import ABC, abstractmethod

# Import Utils
import numpy as np
import tensorflow as tf
from art.estimators.classification import KerasClassifier

class AttackClass(ABC):
    def __init__(self, model, dataset_struct=None, dataset_stats=None, params=None):
        self.model = model
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.params = params

    def create_keras_classifier(self, model):
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        classifier = KerasClassifier(
            model=model,                    # The Keras model
            use_logits=False,               # Use logit outputs instead of probabilities (default: False)
            channel_index=-1,               # Index of the channel axis in the input data (default: -1)
            preprocessing_defences=None,    # Defenses for pre-processing the data (default: None)
            postprocessing_defences=None,   # Defenses for post-processing the results (default: None)
            input_layer=0,                  # Input layer of the model (default: 0)
            output_layer=-1,                # Output layer of the model (default: -1)
            channels_first=False,           # Whether channels are the first dimension in the input data (default: False)
            clip_values=(0, 1)              # Range of valid input values (default: (0,1))
        )
        
        return classifier
    
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

class EvasionAttack(AttackClass):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
        
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

class ExtractionAttack(AttackClass):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def steal_model(self, percentage=0.5):
        # Check if the percentage is between 0 and 1
        if not 0 <= percentage <= 1:
            raise ValueError("Percentage must be between 0 and 1")
            
        # Calculate the number of elements corresponding to the percentage
        total_samples = self.dataset_stats["num_train_samples"]
        stolen_samples = total_samples * percentage
            
        # Setting aside a subset of the source dataset for the original model
        train_data =  self.dataset_struct["train_data"][0]
        train_label = self.dataset_struct["train_label"][1]
            
        x_original = train_data[:stolen_samples]
        y_original = train_label[:stolen_samples]

        # Using the rest of the source dataset for the stolen model
        x_stolen = train_data[stolen_samples:]
        y_stolen = train_label[stolen_samples:]
            
        return (x_original, y_original), (x_stolen, y_stolen)
    
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
    
class InferenceAttack(AttackClass):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
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

from art.utils import to_categorical
from art.attacks.poisoning.perturbations import add_pattern_bd

class BackdoorAttack(AttackClass):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def poison_dataset(self, clean_images, clean_labels, target_labels, backdoor_attack, percent_poison=0.3):
        # Creating copies of our clean images and labels
        # Poisoned samples will be added to these copies
        x_poison = clean_images.copy()
        y_poison = clean_labels.copy()
        
        # Array to indicate if a sample is poisoned or not
        # 0s are for clean samples, 1s are for poisoned samples
        is_poison = np.zeros(shape=y_poison.shape[0])

        # Indicating our source labels (as integers)
        source_labels = np.arange(self.dataset_stats["num_classes"])

        # Iterating over our source labels and provided target labels
        for (source_label, target_label) in (zip(source_labels, target_labels)):
            # Calculating the number of clean labels that are equal to the
            # current source label
            num_labels = np.size(np.where(np.argmax(a=clean_labels, axis=1) == source_label))

            # Calculating the number of samples that should be poisoned from
            # the current source labels
            num_poison = round(percent_poison * num_labels)

            # Getting the images for the current clean label
            source_images = clean_images[np.argmax(a=clean_labels, axis=1) == source_label]

            # Randomly picking indices to poison
            indices_to_be_poisoned = np.random.choice(
                a=num_labels,
                size=num_poison
                )

            # Get the images for the current label that should be poisoned
            images_to_be_poisoned = source_images[indices_to_be_poisoned].copy()

            # Converting the target label to a categorical
            target_label = to_categorical(labels=(np.ones(shape=num_poison) * target_label), nb_classes=self.dataset_stats["num_classes"])

            # Poisoning the images and labels for the current label
            poisoned_images, poisoned_labels = backdoor_attack.poison(
                x=images_to_be_poisoned,
                y=target_label
                )

            # Appending the poisoned images to our clean images
            x_poison = np.append(
                arr=x_poison,
                values=poisoned_images,
                axis=0
                )

            # Appending the poisoned labels to our clean labels
            y_poison = np.append(
                arr=y_poison,
                values=poisoned_labels,
                axis=0
                )

            # Appending 1s to the poison indicator array
            is_poison = np.append(
                arr=is_poison,
                values=np.ones(shape=num_poison)
                )

        # Returning the poisoned samples and the poison indicator array
        return is_poison, x_poison, y_poison
    
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