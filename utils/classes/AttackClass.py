# Utils
import json
import cv2

import numpy as np
from datetime import datetime
from art.utils import to_categorical

# System
import os

# Adversarial Robustness Toolkit
from art.estimators.classification import KerasClassifier

###################################################################################################

# Abstract Class
from abc import ABC, abstractmethod

class AttackClass(ABC):
    def __init__(self, model, dataset_struct=None, dataset_stats=None, params=None):
        self.model = model
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.params = params

    def create_keras_classifier(self, model):
        """
        Create a classifier by wrapping a TensorFlow model in ART's KerasClassifier class.

        Parameters:
        - model (tf.keras.Model): The Keras model to be wrapped.
        - preprocessing_defences (Optional[List], optional): Defenses for pre-processing the data. Default is None.
        - postprocessing_defences (Optional[List], optional): Defenses for post-processing the results. Default is None.

        Returns:
        - classifier (art.classifiers.KerasClassifier): A Keras classifier wrapped with the specified settings.
        """
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
    def perform_attack(self):
        pass
    
    @abstractmethod
    def evaluate(self):
        pass
    
    @abstractmethod
    def plotting_stats(self):
        pass
    
    def save_images(self, tag = "AttackClass", images = [], save_path = "../storage/results", uid = datetime.now().strftime("%Y%m%d%H%M%S%f")):
        """
        Save a list of images to a specified directory with a unique identifier.

        Parameters:
        - tag (str, optional): A tag used for naming the directory and image files. Default is "AttackClass".
        - images (List, optional): A list of images to save. Default is an empty list.
        - save_path (str, optional): The base directory path where images will be saved. Default is "../storage/results".
        - uid (str, optional): A unique identifier for the directory name, typically a timestamp. Default is the current datetime.

        Returns:
        - None
        """
        # Create all directory and file tree
        dirname = f"{tag}-summary-{uid}"
        
        dir_path = os.path.join(save_path, dirname)
        
        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Save sample images
        for i in range(min(len(images), 3)):
            cv2.imwrite(os.path.join(dir_path, f'{tag}_image{i+1}.png'), images[i])
            
    def save_summary(self, tag = "AttackClass", result = {}, images = None, save_path = "../storage/results", uid = datetime.now().strftime("%Y%m%d%H%M%S%f")):
        """
        Save a summary of results, including a JSON file and optional images, to a specified directory.

        Parameters:
        - tag (str, optional): A tag used for naming the directory and files. Default is "AttackClass".
        - result (Dict, optional): A dictionary containing the results to be saved in a JSON file. Default is an empty dictionary.
        - images (Optional[List], optional): A list of images to save. Default is None.
        - save_path (str, optional): The base directory path where the summary and images will be saved. Default is "../storage/results".
        - uid (str, optional): A unique identifier for the directory and file names, typically a timestamp. Default is the current datetime.

        Returns:
        - None
        """
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
    def plotting_stats(self):
        pass

    @abstractmethod
    def result(self):
        pass
    
class ExtractionAttack(AttackClass):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def steal_model(self, percentage=0.5):
        """
        Split the dataset into two parts based on the given percentage: one for the original model and one for the stolen model.

        Parameters:
        - percentage (float, optional): The fraction of the dataset to set aside for the original model. Must be between 0 and 1. Default is 0.5.

        Returns:
        - (x_original, y_original) (Tuple): A tuple containing the data and labels for the original model.
        - (x_stolen, y_stolen) (Tuple): A tuple containing the data and labels for the stolen model.
        """
        # Check if the percentage is between 0 and 1
        if not 0 <= percentage <= 1:
            raise ValueError("Percentage must be between 0 and 1")
            
        # Calculate the number of elements corresponding to the percentage
        total_samples = self.dataset_stats["num_train_samples"]
        stolen_samples = int(total_samples * percentage)
        
        # Setting aside a subset of the source dataset for the original model
        train_data =  self.dataset_struct["train_data"][0]
        train_label = self.dataset_struct["train_data"][1]
            
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
    def plotting_stats(self):
        pass
    
    @abstractmethod
    def result(self):
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
    def plotting_stats(self):
        pass

    @abstractmethod
    def result(self):
        pass

class BackdoorAttack(AttackClass):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def poison_dataset(self, clean_images, clean_labels, target_labels, backdoor_attack, poisoned_percentage=0.3):
        """
        Poison a portion of the dataset by injecting backdoor samples with target labels.

        Parameters:
        - clean_images (np.ndarray): Array of clean images.
        - clean_labels (np.ndarray): Array of labels corresponding to the clean images.
        - target_labels (List[int]): List of target labels for poisoning, one for each source label.
        - backdoor_attack: An instance of a backdoor attack class, containing a poison method to apply to the images.
        - poisoned_percentage (float, optional): The fraction of samples to poison for each source label. Default is 0.3.

        Returns:
        - is_poison (np.ndarray): An array indicating which samples are poisoned (1 for poisoned, 0 for clean).
        - x_poison (np.ndarray): The dataset containing both clean and poisoned images.
        - y_poison (np.ndarray): The labels corresponding to the `x_poison` dataset, including both clean and poisoned labels.
        """
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
            num_poison = round(poisoned_percentage * num_labels)

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
    def plotting_stats(self):
        pass
    
    @abstractmethod
    def result(self):
        pass