# CopycatCNN ART Class 
from art.attacks.extraction import CopycatCNN as CopycatCNN_ART

# Own Modules
from classes.AttackClass import ExtractionAttack

# Utils
from utils.model import *

TAG = "CopycatCNN"

class CopycatCNN(ExtractionAttack):
    """
    Copycat CNN attack class.

    This class implements the Copycat CNN attack for extracting a model's knowledge by querying it with
    a stolen dataset. The attack aims to replicate the functionality of the original model by training
    a new model on the queries made to the victim model.
    
    Paper: https://arxiv.org/abs/1806.05476
    """
    def __init__(self, model, dataset_struct, dataset_stats, params):
        """
        Initialize the CopycatCNN attack instance.

        Parameters:
        - model (tf.keras.Model): The Keras model to attack.
        - dataset_struct (Dict[str, tf.Tensor]): Dictionary containing training and test data.
        - dataset_stats (Dict[str, Any]): Dictionary containing dataset statistics.
        - params (Dict[str, Any]): Dictionary containing parameters for the attack.
        """
        super().__init__(model, dataset_struct, dataset_stats, params)
        
    def perform_attack(self, original_dataset, stolen_dataset):
        """
        Perform the Copycat CNN attack by training a model on the original dataset and then extracting
        a copycat model using the stolen dataset.

        Parameters:
        - original_dataset (Tuple[tf.Tensor, tf.Tensor]): Tuple containing the training data and labels
          for training the original model.
        - stolen_dataset (Tuple[tf.Tensor, tf.Tensor]): Tuple containing the data to query the victim model
          and use for training the stolen model.

        Returns:
        - Tuple[tf.keras.Model, tf.keras.Model]: A tuple containing the original model and the thieved
          (stolen) model.
        """
        # Fit of the model on the original dataset
        print(f"[{TAG}] Fit of the model on the original dataset")
        original_model = fit_model(original_dataset, copy_model(self.model), self.params["batch_size"], self.params["epochs"])
        
        # Wrapping the model in the ART KerasClassifier class
        print(f"[{TAG}] Wrapping the model in the ART KerasClassifier class")
        classifier_original = self.create_keras_classifier(original_model)
                
        # Creating the "neural net thief" object that will steal the original classifier
        print(f"[{TAG}] Creating the 'neural net thief' object that will steal the original classifier")
        copycat_cnn = CopycatCNN_ART(
            classifier=classifier_original,                 # A victim classifier
            batch_size_fit=self.params["batch_size"],       # Size of batches for fitting the thieved classifier (default: 1)
            batch_size_query=self.params["batch_size"],     # Size of batches for querying the victim classifier (default: 1)
            nb_epochs=self.params["epochs"],                # Number of epochs to use for training (default: 10)
            nb_stolen=len(stolen_dataset[0]),               # Number of queries submitted to the victim classifier to steal it (default: 1)
            use_probability=self.params["use_probability"]  # Use probability (default: False)
        )
        
        # Wrapping the model in the ART KerasClassifier class
        print(f"[{TAG}] Wrapping the model in the ART KerasClassifier class")
        model_stolen = self.create_keras_classifier(self.model)
                                               
        # Extracting a thieved classifier by training the reference model
        print(f"[{TAG}] Extracting a thieved classifier by training the reference model")
        classifier_stolen = copycat_cnn.extract(
            x=stolen_dataset[0],                # An array with the source input to the victim classifier
            y=stolen_dataset[1],                # Target values (class labels) one-hot-encoded of shape (nb_samples, nb_classes) or indices of shape (nb_samples,). Not used in this attack
            thieved_classifier=model_stolen     # A classifier to be stolen, currently always trained on one-hot labels
            )
        
        return classifier_original, classifier_stolen
        
    def evaluate(self, original_classifier, stolen_classifier):
        """
        Evaluate the performance of the original and stolen classifiers on the test dataset.

        Parameters:
        - original_classifier (tf.keras.Model): The original model that was used for extraction.
        - stolen_classifier (tf.keras.Model): The thieved (stolen) model obtained from the Copycat CNN attack.

        Returns:
        - Tuple[Tuple[float, float], Tuple[float, float]]: Performance scores of the original and stolen
          classifiers, respectively.
        """
        # Testing the performance of the original classifier
        print(f"[{TAG}] Testing the performance of the original classifier")
        score_original = original_classifier._model.evaluate(
            x=self.dataset_struct["test_data"][0],
            y=self.dataset_struct["test_data"][1]
            )

        # Testing the performance of the stolen classifier
        print(f"[{TAG}] Testing the performance of the stolen classifier")
        score_stolen = stolen_classifier._model.evaluate(
            x=self.dataset_struct["test_data"][0],
            y=self.dataset_struct["test_data"][1]
            )
        
        return score_original, score_stolen
        
    def plotting_stats(self):
        """
        This method is not implemented. It should handle plotting statistics if required.

        Raises:
        - NotImplementedError: This method has not been implemented yet.
        """
        raise NotImplementedError
    
    def result(self, score_original, score_stolen):
        """
        Print and save the results of the attack evaluation.

        Parameters:
        - score_original (Tuple[float, float]): Loss and accuracy scores of the original model.
        - score_stolen (Tuple[float, float]): Loss and accuracy scores of the stolen model.

        Returns:
        - result_dict (Dict[str, Any]): Dictionary containing the results of the attack.
        """
        # Comparing test losses
        print(f"Original test loss: {score_original[0]:.2f} "
            f"vs stolen test loss: {score_stolen[0]:.2f}")

        # Comparing test accuracies
        print(f"Original test accuracy: {score_original[1]:.2f} "
            f"vs stolen test accuracy: {score_stolen[1]:.2f}")
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "original_scores": {
                "loss": f"{score_original[0]:.2f}",
                "accuracy": f"{score_original[1]:.2f}"
            },
            "stolen_scores": {
                "loss": f"{score_stolen[0]:.2f}",
                "accuracy": f"{score_stolen[1]:.2f}"
            },
            "params": self.params,
            "summary": summary
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
