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

'''
Implementation of a postprocessor based on adding the Reverse Sigmoid perturbation to classifier output.
'''

TAG = "ReverseSigmoid"

class ReverseSigmoid(PostprocessorDefense):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def victim_model_perform(self, train_images_victim, train_labels_victim):
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
        
    def perform_defense(self, use_probability):
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
        # Getting predictions for the unprotected model
        print(f"[{TAG}] Getting predictions for the unprotected model")
        unprotected_predictions = unprotected_classifier.predict(x=self.dataset_struct["test_data"][0][:10])
        
        # Getting predictions for the protected model
        print(f"[{TAG}] Getting predictions for the protected model")
        protected_predictions = protected_classifier.predict(x=self.dataset_struct["test_data"][0])

        return unprotected_predictions, protected_predictions
    
    def evaluate_probabilistic(self, classifier_stolen_unprotected_probabilistic, classifier_stolen_protected_probabilistic):
        # Evaluating the performance of the victim model and the stolen models
        print(f"[{TAG}] Evaluating the performance of the victim model and the stolen models")
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        score_stolen_unprotected_probabilistic = classifier_stolen_unprotected_probabilistic._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_protected_probabilistic = classifier_stolen_protected_probabilistic._model.evaluate(x=test_images_original, y=test_labels_original)
        
        return score_stolen_unprotected_probabilistic, score_stolen_protected_probabilistic

    def evaluate(self, unprotected_classifier, classifier_stolen_unprotected, classifier_stolen_protected):
        # Evaluating the performance of the victim model and the stolen models
        print(f"[{TAG}] Evaluating the performance of the victim model and the stolen models")
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        score_victim = unprotected_classifier._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_unprotected = classifier_stolen_unprotected._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_protected = classifier_stolen_protected._model.evaluate(x=test_images_original, y=test_labels_original)

        return score_victim, score_stolen_unprotected, score_stolen_protected
    
    def plotting_stats(self):
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
            "summary": summary
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(TAG, result_dict)
        
        return result_dict
