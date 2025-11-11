# CopycatCNN & ReverseSigmoid ART Class
from art.attacks.extraction import CopycatCNN as CopycatCNN_ART
from art.defences.postprocessor import ReverseSigmoid as ReverseSigmoid_ART

# Support
import numpy as np

# Own Modules
from ml_attacks.extraction.CopycatCNN import CopycatCNN
from classes.DefenseClass import PostprocessorDefense

# Utils
from utils.model import *

TAG = "ReverseSigmoid"

class ReverseSigmoid(PostprocessorDefense):
    """
    Implementation of a post-processor defense based on the Reverse Sigmoid perturbation applied to the output of the classifier.

    The Reverse Sigmoid defense modifies the classifier predictions by adding a Reverse Sigmoid perturbation.
    This perturbation can help protect the model from extraction attacks, such as the CopycatCNN.
    """
    def __init__(self, model, dataset_struct, dataset_stats, params):
        """
        Initialize the ReverseSigmoid defense instance.

        Parameters:
        - model (tf.keras.Model): The Keras model to protect.
        - dataset_struct (Dict[str, np.ndarray]): Dictionary containing training and test data.
        - dataset_stats (Dict[str, Any]): Dictionary containing dataset statistics.
        - params (Dict[str, Any]): Dictionary containing parameters for the defense, including Reverse Sigmoid parameters.
        """
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def victim_model_perform(self, train_images_victim, train_labels_victim):
        """
        Train the victim model and create classifiers with and without the Reverse Sigmoid postprocessor.

        Parameters:
        - train_images_victim (np.ndarray): Training images for the victim model.
        - train_labels_victim (np.ndarray): Training labels for the victim model.

        Returns:
        - Tuple[tf.keras.Model, tf.keras.Model]: The unprotected and protected classifiers.
        """
        # Fit the given model
        print(f"[{TAG}] Fit the given model")
        fitted_model = fit_model((train_images_victim,train_labels_victim), copy_model(self.model), self.params["batch_size"], self.params["epochs"])
        
        # Initializing the postprocessor
        print(f"[{TAG}] Initializing the postprocessor")
        postprocessor = ReverseSigmoid_ART(
            beta=self.params["beta"],       # The beta parameter for the Reverse Sigmoid function (default: 1.0)
            gamma=self.params["gamma"],     # The gamma parameter for the Reverse Sigmoid function (default: 0.1)
            apply_fit=False,                # If True, the defense is applied during the fit (default: False)
            apply_predict=True              # If True, the defense is applied during prediction (default: True)
        )
        
        # Creating an instance of an unprotected classifier
        print(f"[{TAG}] Creating an instance of an unprotected classifier")
        unprotected_classifier = self.create_keras_classifier(fitted_model)
        
        # Creating an instance of a protected classifier
        print(f"[{TAG}] Creating an instance of a protected classifier")
        protected_classifier = self.create_keras_classifier(model=fitted_model, postprocessing_defences=postprocessor)
        
        return unprotected_classifier, protected_classifier
    
    def stolen_model_perform(self, unprotected_classifier, protected_classifier, train_images_stolen, train_labels_stolen, probabilistic=False):
        """
        Perform the CopycatCNN attack to extract models from the given classifiers.

        Parameters:
        - unprotected_classifier (tf.keras.Model): The classifier without postprocessing.
        - protected_classifier (tf.keras.Model): The classifier with Reverse Sigmoid postprocessing.
        - train_images_stolen (np.ndarray): Images used to train the extractor.
        - train_labels_stolen (np.ndarray): Labels corresponding to the training images.
        - probabilistic (bool): If True, use probabilistic extraction; otherwise, use deterministic.

        Returns:
        - Tuple[tf.keras.Model, tf.keras.Model]: Extracted models from the unprotected and protected classifiers.
        """
        # Initializing the models that will be trained by the model extractor
        print(f"[{TAG}] Initializing the models that will be trained by the model extractor")
        model_stolen_unprotected = self.create_keras_classifier(model=self.model)
        model_stolen_protected = self.create_keras_classifier(model=self.model)

        # Creating the "neural net thief" object that will try to steal the unprotected classifier
        print(f"[{TAG}] Creating the 'neural net thief' object that will try to steal the unprotected classifier")
        copycat_cnn_unprotected = CopycatCNN_ART(
            batch_size_fit=self.params["batch_size"],
            batch_size_query=self.params["batch_size"],
            nb_epochs=self.params["epochs"],
            nb_stolen=len(train_images_stolen),
            use_probability=probabilistic,
            classifier=unprotected_classifier
            )

        # Creating the "neural net thief" object that will try to steal the protected classifier
        print(f"[{TAG}] Creating the 'neural net thief' object that will try to steal the protected classifier")
        copycat_cnn_protected = CopycatCNN_ART(
            batch_size_fit=self.params["batch_size"],
            batch_size_query=self.params["batch_size"],
            nb_epochs=self.params["epochs"],
            nb_stolen=len(train_images_stolen),
            use_probability=probabilistic,
            classifier=protected_classifier
            )
        
        # Extracting the unprotected model
        print(f"[{TAG}] Extracting the unprotected model")
        classifier_stolen_unprotected = copycat_cnn_unprotected.extract(
            x=train_images_stolen,
            y=train_labels_stolen,
            thieved_classifier=model_stolen_unprotected
        )
            
        # Extracting the protected model
        print(f"[{TAG}] Extracting the protected model")
        classifier_stolen_protected = copycat_cnn_protected.extract(
            x=train_images_stolen,
            y=train_labels_stolen,
            thieved_classifier=model_stolen_protected
        )
            
        return classifier_stolen_unprotected, classifier_stolen_protected
        
    def perform_defense(self, use_probability = False):
        """
        Perform the defense by training models and extracting them using CopycatCNN attack.

        Parameters:
        - use_probability (bool): If True, use probabilistic extraction; otherwise, use deterministic.

        Returns:
        - Tuple[Tuple[tf.keras.Model, tf.keras.Model], Tuple[tf.keras.Model, tf.keras.Model]]:
          - The unprotected and protected classifiers.
          - The extracted models from the unprotected and protected classifiers.
        """
        # Initialize a CopycatCNN attack
        print(f"[{TAG}] Initialize a CopycatCNN attack")
        attack_params = self.params["extraction_params"]
        
        copycatCNN_attack = CopycatCNN(self.model, self.dataset_struct, self.dataset_stats, attack_params)
        
        # Setting aside a subset of the source dataset for the original model and using the rest of the source dataset for the stolen model
        print(f"[{TAG}] Setting aside a subset of the source dataset for the original model and using the rest of the source dataset for the stolen model")
        train_victim, train_stolen =  copycatCNN_attack.steal_model()

        train_images_victim = train_victim[0]
        train_labels_victim = train_victim[1]
        
        train_images_stolen = train_stolen[0]
        train_labels_stolen = train_stolen[1]
        
        # Perform victim model and stolen model postprocessor attack
        print(f"[{TAG}] Perform victim model and stolen model postprocessor attack")
        unprotected_classifier, protected_classifier = self.victim_model_perform(train_images_victim, train_labels_victim)
        classifier_stolen_unprotected, classifier_stolen_protected = self.stolen_model_perform(unprotected_classifier, protected_classifier, train_images_stolen, train_labels_stolen, probabilistic=use_probability)

        return (unprotected_classifier, protected_classifier), (classifier_stolen_unprotected, classifier_stolen_protected)
    
    def evaluate_prediction(self, unprotected_classifier, protected_classifier):
        """
        Evaluate and compare predictions made by the unprotected and protected classifiers.

        Parameters:
        - unprotected_classifier (tf.keras.Model): The classifier without postprocessing.
        - protected_classifier (tf.keras.Model): The classifier with Reverse Sigmoid postprocessing.

        Returns:
        - Tuple[np.ndarray, np.ndarray]: Predictions from the unprotected and protected classifiers.
        """
        # Getting predictions for the unprotected model
        print(f"[{TAG}] Getting predictions for the unprotected model")
        unprotected_predictions = unprotected_classifier.predict(x=self.dataset_struct["test_data"][0][:10])
        
        # Getting predictions for the protected model
        print(f"[{TAG}] Getting predictions for the protected model")
        protected_predictions = protected_classifier.predict(x=self.dataset_struct["test_data"][0])

        return unprotected_predictions, protected_predictions
    
    def evaluate_probabilistic(self, classifier_stolen_unprotected_probabilistic, classifier_stolen_protected_probabilistic):
        """
        Evaluate the performance of the probabilistic models extracted from the unprotected and protected classifiers.

        Parameters:
        - classifier_stolen_unprotected_probabilistic (tf.keras.Model): The probabilistic model extracted from the unprotected classifier.
        - classifier_stolen_protected_probabilistic (tf.keras.Model): The probabilistic model extracted from the protected classifier.

        Returns:
        - Tuple[Tuple[float, float], Tuple[float, float]]: Performance metrics (loss, accuracy) for the extracted probabilistic models.
        """
        # Evaluating the performance of the victim model and the stolen models
        print(f"[{TAG}] Evaluating the performance of the victim model and the stolen models")
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        score_stolen_unprotected_probabilistic = classifier_stolen_unprotected_probabilistic._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_protected_probabilistic = classifier_stolen_protected_probabilistic._model.evaluate(x=test_images_original, y=test_labels_original)
        
        return score_stolen_unprotected_probabilistic, score_stolen_protected_probabilistic

    def evaluate(self, unprotected_classifier, classifier_stolen_unprotected, classifier_stolen_protected):
        """
        Evaluate the performance of the victim model and the stolen models.

        Parameters:
        - unprotected_classifier (tf.keras.Model): The unprotected classifier model.
        - classifier_stolen_unprotected (tf.keras.Model): The stolen model extracted from the unprotected classifier.
        - classifier_stolen_protected (tf.keras.Model): The stolen model extracted from the protected classifier.

        Returns:
        - Tuple[float, float, float]: The loss and accuracy scores for the unprotected model, stolen unprotected model, and stolen protected model.
        """
        # Evaluating the performance of the victim model and the stolen models
        print(f"[{TAG}] Evaluating the performance of the victim model and the stolen models")
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        score_victim = unprotected_classifier._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_unprotected = classifier_stolen_unprotected._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_protected = classifier_stolen_protected._model.evaluate(x=test_images_original, y=test_labels_original)

        return score_victim, score_stolen_unprotected, score_stolen_protected
    
    def plotting_stats(self):
        """
        This method is not implemented. It should handle plotting statistics if required.

        Raises:
        - NotImplementedError: This method has not been implemented yet.
        """
        raise NotImplementedError
    
    def stats_prediction(self, unprotected_predictions, protected_predictions):
        # Inspecting unprotected predictions
        print(f"[{TAG}] Inspecting unprotected predictions")
        print("----- ONE-HOT PREDICTIONS -----", "\n", unprotected_predictions, "\n")
        print("----- CLASS PREDICTIONS -----", "\n", np.argmax(a=unprotected_predictions, axis=1))
        
        # Inspecting protected predictions
        print(f"[{TAG}] Inspecting protected predictions")
        print("----- ONE-HOT PREDICTIONS -----", "\n", protected_predictions, "\n")
        print("----- CLASS PREDICTIONS -----", "\n", np.argmax(a=protected_predictions, axis=1))
    
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "unprotected": {
                "one_hot_predictions": f"{unprotected_predictions}",
                "class_predictions": f"{np.argmax(a=unprotected_predictions, axis=1)}"
            },
            "protected": {
                "one_hot_predictions": f"{protected_predictions}",
                "class_predictions": f"{np.argmax(a=protected_predictions, axis=1)}"
            },
            "summary": summary
        }
        
        return result_dict
    
    def stats_probabilistic(self, score_victim, score_stolen_unprotected_probabilistic, score_stolen_protected_probabilistic):
        # Checking Test Metrics Original vs Probabilistic Stolen Models
        print(f"[{TAG}] Checking Test Metrics Original vs Probabilistic Stolen Models")
        
        # Comparing test losses
        print(f"Original model loss: {score_victim[0]:.2f}\n"
            f"Stolen unprotected model loss: {score_stolen_unprotected_probabilistic[0]:.2f}\n"
            f"Stolen protected model loss: {score_stolen_protected_probabilistic[0]:.2f}\n")

        # Comparing test accuracies
        print(f"Original model accuracy: {score_victim[1]:.2f}\n"
            f"Stolen unprotected model accuracy: {score_stolen_unprotected_probabilistic[1]:.2f}\n"
            f"Stolen protected model accuracy: {score_stolen_protected_probabilistic[1]:.2f}\n")

        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "loss": {
                "original_model": f"{score_victim[0]:.2f}",
                "stolen_unprotected": f"{score_stolen_unprotected_probabilistic[0]:.2f}",
                "stolen_protected": f"{score_stolen_protected_probabilistic[0]:.2f}"
            },
            "accuracy": {
                "original_model": f"{score_victim[1]:.2f}",
                "stolen_unprotected": f"{score_stolen_unprotected_probabilistic[1]:.2f}",
                "stolen_protected": f"{score_stolen_protected_probabilistic[1]:.2f}"
            },
            "summary": summary,
        }
        
        return result_dict
    
    def result(self, score_victim, score_stolen_unprotected, score_stolen_protected):
        # Checking Test Metrics Original vs Stolen Models
        print(f"[{TAG}] Checking Test Metrics Original vs Stolen Models")
        
        # Comparing test losses
        print(f"Original model loss: {score_victim[0]:.2f}\n"
            f"Stolen unprotected model loss: {score_stolen_unprotected[0]:.2f}\n"
            f"Stolen protected model loss: {score_stolen_protected[0]:.2f}\n")

        # Comparing test accuracies
        print(f"Original model accuracy: {score_victim[1]:.2f}\n"
            f"Stolen unprotected model accuracy: {score_stolen_unprotected[1]:.2f}\n"
            f"Stolen protected model accuracy: {score_stolen_protected[1]:.2f}\n")
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "loss": {
                "original_model": f"{score_victim[0]:.2f}",
                "stolen_unprotected": f"{score_stolen_unprotected[0]:.2f}",
                "stolen_protected": f"{score_stolen_protected[0]:.2f}"
            },
            "accuracy": {
                "original_model": f"{score_victim[1]:.2f}",
                "stolen_unprotected": f"{score_stolen_unprotected[1]:.2f}",
                "stolen_protected": f"{score_stolen_protected[1]:.2f}"
            },
            "params": self.params,
            "summary": summary
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(TAG, result_dict)
        
        return result_dict
