# MIFace ART Class
from art.attacks.inference.model_inversion import MIFace as MIFace_ART

# Support
import numpy as np
from datetime import datetime

# Own Modules
from classes.AttackClass import InferenceAttack

# Utils
from utils.model import *

TAG = "MIFace"

class MIFace(InferenceAttack):
    """
    MIFace attack class.

    This class implements the MIFace attack for model inversion, which reconstructs images of each class
    based on the gradients obtained from the target model. The algorithm is designed to work with
    classifiers that expose class gradients, typically in models with continuous features.

    Paper: https://dl.acm.org/doi/10.1145/2810103.2813677
    """
    def __init__(self, model, dataset_struct, dataset_stats, params):
        """
        Initialize the MIFace attack instance.

        Parameters:
        - model (tf.keras.Model): The Keras model to attack.
        - dataset_struct (Dict[str, tf.Tensor]): Dictionary containing training and test data.
        - dataset_stats (Dict[str, Any]): Dictionary containing dataset statistics.
        - params (Dict[str, Any]): Dictionary containing parameters for the attack.
        """
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def perform_attack(self):
        """
        Perform the MIFace attack to invert the model and reconstruct images for each class.

        Returns:
        - np.ndarray: The reconstructed images for each class.
        """
        # Create a Keras Classifier
        print(f"[{TAG}] Create a Keras Classifier")
        extraction_classifier = self.create_keras_classifier(self.model)
        
        # Defining a model inversion attack
        print(f"[{TAG}] Defining a model inversion attack")
        attack = MIFace_ART(
            classifier=extraction_classifier,               # The classifier used for crafting adversarial examples (default: CLASSIFIER_LOSS_GRADIENTS_TYPE)
            max_iter=self.params["max_iter"],               # Maximum number of gradient descent iterations for the model inversion (default: 10000)
            window_length=self.params["window_length"],     # Length of window for checking whether descent should be aborted (default: 100)
            threshold=self.params["threshold"],             # Threshold for descent stopping criterion (default: 0.99)
            learning_rate=self.params["learning_rate"],     # Learning rate (default: 0.1)
            batch_size=self.params["batch_size"],           # Size of internal batches (default: 256)
            verbose=True                                    # Print debug information during execution (default: True)
        )
    
        # Get some dataset stats
        print(f"[{TAG}] Get some dataset stats")
        num_classes = self.dataset_stats["num_classes"]
        
        image_shape = self.dataset_stats["image_shape"]
        shape_x = image_shape[0]
        shape_y = image_shape[1]
        channels = image_shape[2]
        
        print(f"[{TAG}] Stats:\n N° Classes: {num_classes}\n Image Shape: {image_shape}")
        
        # Defining the target labels for model inversion
        print(f"[{TAG}] Defining the target labels for model inversion")
        target = np.arange(start=0, stop=num_classes)
        
        print(f"[{TAG}] Target Labels: {target}")
        
        # Defining an initialization array for model inversion
        print(f"[{TAG}]")
        x_init_average = np.zeros(shape=(num_classes, shape_x, shape_y, channels)) + np.mean(a=self.dataset_struct["test_data"][0], axis=0)
        
        # Checking class gradients
        print(f"[{TAG}] Checking class gradients")
        class_gradient = extraction_classifier.class_gradient(
            x=x_init_average,
            label=target
            )
        
        # Reshaping class gradients
        print(f"[{TAG}] Reshaping class gradients")
        class_gradient = np.reshape(
            a=class_gradient,
            newshape=(num_classes, shape_x*shape_y*channels)
            )

        # Obtaining the largest gradient value for each class
        print(f"[{TAG}] Obtaining the largest gradient value for each class")
        class_gradient_max = np.max(class_gradient, axis=1)

        print(f"[{TAG}] Class Gradient Max:\n {class_gradient_max}")
        
        # Running model inversion
        # %%time
        print(f"[{TAG}] Running model inversion")
        x_infer_from_average = attack.infer(
            x=x_init_average,
            y=target
            )
        
        return  x_infer_from_average
    
    def evaluate(self, miface_inverted_dataset):
        """
        Evaluate the results of the model inversion attack.

        Parameters:
        - miface_inverted_dataset (np.ndarray): The reconstructed images from the model inversion.

        Returns:
        - Tuple[np.ndarray, int]: The reconstructed images and their count.
        """
        # Get Inverted Images
        print(f"[{TAG}] Get Inverted Images")
        print(f"Images inverted count: {len(miface_inverted_dataset)}")
        return (miface_inverted_dataset, len(miface_inverted_dataset))
    
    def plotting_stats(self):
        """
        This method is not implemented. It should handle plotting statistics if required.

        Raises:
        - NotImplementedError: This method has not been implemented yet.
        """
        raise NotImplementedError
    
    def result(self, miface_data):
        """
        Print and save the results of the attack, including reconstructed images.

        Parameters:
        - miface_data (Tuple[np.ndarray, int]): The reconstructed images and their count.

        Returns:
        - Dict[str, Any]: A dictionary containing the results of the attack.
        """
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "params": self.params,
            "summary": summary
        }
    
        # Save summary files
        print(f"[{TAG}] Save summary files")
        uid = datetime.now().strftime("%Y%m%d%H%M%S%f")
        save_path = "../storage/results"
        self.save_summary(tag=TAG, result=result_dict, images=miface_data[0], save_path=save_path, uid=uid)
            
        return result_dict
