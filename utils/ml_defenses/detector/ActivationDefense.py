# ActivationDefence ART Class
from art.defences.detector.poison import ActivationDefence as ActivationDefence_ART

# Support
import json
import pprint
import numpy as np

# Own Modules
from ml_attacks.poisoning.CleanLabelBackdoor import CleanLabelBackdoor
from ml_attacks.poisoning.SimpleBackdoor import SimpleBackdoor
from classes.DefenseClass import TransformerDefense

# Utils
from utils.model import *

TAG = "ActivationDefense"

class ActivationDefense(TransformerDefense):
    """
    Activation Defense class for detecting poisoned samples based on activation clustering.

    This class implements a defense strategy based on the clustering of activations to detect
    poisoning attacks, such as backdoor attacks.

    Please keep in mind the limitations of defences. For more information on the limitations of this defence, see https://arxiv.org/abs/1905.13409.
    For details on how to evaluate classifier security in general, see https://arxiv.org/abs/1902.06705.
    
    Paper: https://arxiv.org/abs/1811.03728
    """
    def __init__(self, model, dataset_struct, dataset_stats, params):
        """
        Initialize the Activation Defense defense instance.

        Parameters:
        - model (tf.keras.Model): The Keras model to defend.
        - dataset_struct (Dict[str, tf.Tensor]): Dictionary containing training and test data.
        - dataset_stats (Dict[str, Any]): Dictionary containing dataset statistics.
        - params (Dict[str, Any]): Dictionary containing parameters for the defense.
        """
        super().__init__(model, dataset_struct, dataset_stats, params)
        
    def perform_defense(self):
        """
        Perform the defense by detecting poisoned samples using activation clustering.

        Returns:
        - Tuple: Contains the following elements:
            - clean_test (Tuple[np.ndarray, np.ndarray]): Clean test images and labels.
            - poisoned_test (Tuple[np.ndarray, np.ndarray]): Poisoned test images and labels.
            - is_poisoned_stats (Tuple[np.ndarray, np.ndarray, np.ndarray]): Poisoning status of training and test data, and shuffled indices.
            - model_poisoned (tf.keras.Model): The trained model with poisoned data.
            - report (Dict[str, Any]): The defense report including clustering results.
            - is_clean_reported (np.ndarray): Array indicating if samples are clean or not according to the defense.
            - defense (ActivationDefence_ART): The defense object used for poisoning detection.
        """
        # Defining new target labels
        print(f"[{TAG}] Defining new target labels")
        num_classes = self.dataset_stats["num_classes"]
        random_label = np.random.randint(0, num_classes)
        
        target_labels = np.array([random_label] * num_classes)

        
        print(f"[{TAG}] Initializing a Poisoning attack")
        attack = self.params["poison_attack"]
        attack_params = {
            "epochs": self.params["epochs"],
            "batch_size": self.params["batch_size"],
            "poisoned_percentage": self.params["poisoned_percentage"],
            "target_labels": target_labels
        }
        if(attack.lower() == "cleanlabel"):
            # Defining a clean label backdoor attack
            backdoor_attack = CleanLabelBackdoor(model=self.model,
                                                dataset_struct=self.dataset_struct,
                                                dataset_stats=self.dataset_stats,
                                                params=attack_params)
        elif(attack.lower() == "simple"):
            # Defining a poisoning backdoor attack
            backdoor_attack = SimpleBackdoor(model=self.model,
                                             dataset_struct=self.dataset_struct,
                                             dataset_stats=self.dataset_stats,
                                             params=attack_params)
        else:
            #backdoor_class = None
            backdoor_attack = None
        
        clean_test, poisoned_test, is_poisoned_stats, model_poisoned = backdoor_attack.perform_attack(target_lbl=target_labels)
        
        # Evaluating the performance of the vulnerable classifier on clean and poisoned images
        #print(f"[{TAG}] Evaluating the performance of the vulnerable classifier on clean and poisoned images")
        #backdoor_attack.evaluate(clean_test, poisoned_test, model_poisoned)
        
        # Wrapping the model in KerasClassifier
        print(f"[{TAG}] Wrapping the model in KerasClassifier")
        classifier_poisoned = self.create_keras_classifier(model_poisoned)
        
        # Initializing a defense object
        print(f"[{TAG}] Initializing a defense object")
        defense = ActivationDefence_ART(
            classifier=classifier_poisoned,                 # The classifier on which to apply the defense
            x_train=self.dataset_struct["train_data"][0],   # The training images
            y_train=self.dataset_struct["train_data"][1],   # The training labels
            generator=None,                                 # A DataGenerator object (default: None)
            ex_re_threshold=None                            # A threshold float (default: None)
            )
        
        # Detecting poisoned samples in the provided images
        print(f"[{TAG}] Detecting poisoned samples in the provided images")
        report, is_clean_reported = defense.detect_poison(
            clustering_method="KMeans",
            nb_clusters=self.params["nb_clusters"],
            nb_dims=self.params["nb_dims"],
            reduce=self.params["reduce"],
            cluster_analysis=self.params["cluster_analysis"]
            )
        
        return clean_test, poisoned_test, is_poisoned_stats, model_poisoned, (report, is_clean_reported), defense
    
    def evaluate_report(self, report_stats, is_poisoned_stats, defense):
        """
        Evaluate and inspect the defense report and confusion matrix.

        Parameters:
        - report_stats (Tuple[Dict[str, Any], np.ndarray]): The defense report and clean indicator array.
        - is_poisoned_stats (Tuple[np.ndarray, np.ndarray, np.ndarray]): Poisoning status of training and test data, and shuffled indices.
        - defense (ActivationDefence_ART): The defense object used for poisoning detection.

        Returns:
        - Tuple: Contains the following elements:
            - confusion_matrix (Dict[str, Any]): The confusion matrix for the defense evaluation.
            - sprites_by_class (Dict[str, np.ndarray]): Visualizations of clusters by class.
        """
        # Inspecting the report
        print(f"[{TAG}] Inspecting the report")
        pprint.pprint(report_stats[0])

        # Inverting our poison indicator array
        # so that clean samples are indicated as "True" (1)
        # and poisoned samples as "False" (0)
        print(f"[{TAG}] Inverting our poison indicator array")
        is_poison_train = is_poisoned_stats[0]
        is_poison_test = is_poisoned_stats[1]
        is_clean = (is_poison_test == 0)

        # Generating a confusion matrix to evaluate defenses
        print(f"[{TAG}] Generating a confusion matrix to evaluate defenses")
        shuffled_indices = is_poisoned_stats[2]
        confusion_matrix = defense.evaluate_defence(is_clean=is_clean[shuffled_indices])

        # Getting the visualizations for clusters
        print(f"[{TAG}] Getting the visualizations for our clusters")
        sprites_by_class = defense.visualize_clusters(
            x_raw=self.dataset_struct["train_data"][0],
            save=False
        )
        
        return (confusion_matrix, sprites_by_class)
    
    def evaluate_metrics(self, clean_test, poisoned_test, model_poisoned):
        """
        Evaluate the performance of the trained model on clean and poisoned samples.

        Parameters:
        - clean_test (Tuple[np.ndarray, np.ndarray]): Clean test images and labels.
        - poisoned_test (Tuple[np.ndarray, np.ndarray]): Poisoned test images and labels.
        - model_poisoned (tf.keras.Model): The trained model with poisoned data.

        Returns:
        - Tuple: Contains the following elements:
            - score_clean (Tuple[float, float]): Loss and accuracy on clean test data.
            - score_poisoned (Tuple[float, float]): Loss and accuracy on poisoned test data.
        """
        # Evaluating the performance of the vulnerable classifier on clean and poisoned samples
        print(f"[{TAG}] Evaluating the performance of the vulnerable classifier on clean and poisoned samples")
        score_clean = model_poisoned.evaluate(x=clean_test[0], y=clean_test[1])
        score_poisoned = model_poisoned.evaluate(x=poisoned_test[0], y=poisoned_test[1])
        
        return (score_clean, score_poisoned)
    
    def evaluate(self, clean_test, poisoned_test, is_poisoned_stats, model_poisoned, report_stats, defense):
        """
        Evaluate the performance of the trained model on clean and poisoned samples.

        Parameters:
        - clean_test (Tuple[np.ndarray, np.ndarray]): Clean test images and labels.
        - poisoned_test (Tuple[np.ndarray, np.ndarray]): Poisoned test images and labels.
        - model_poisoned (tf.keras.Model): The trained model with poisoned data.

        Returns:
        - Tuple: Contains the following elements:
            - score_clean (Tuple[float, float]): Loss and accuracy on clean test data.
            - score_poisoned (Tuple[float, float]): Loss and accuracy on poisoned test data.
        """
        # Evaluate attack metrics
        print(f"[{TAG}] Evaluate attack metrics")
        attack_metrics = self.evaluate_metrics(clean_test, poisoned_test, model_poisoned)
        
        # Evaluate defense metrics
        print(f"[{TAG}] Evaluate defense metrics")
        defense_metrics = self.evaluate_report(report_stats, is_poisoned_stats, defense)
        
        return attack_metrics, defense_metrics
            
    def plotting_stats(self):
        """
        This method is not implemented. It should handle plotting statistics if required.

        Raises:
        - NotImplementedError: This method has not been implemented yet.
        """
        raise NotImplementedError
    
    def result(self, attack_metrics, defense_metrics):
        """
        Evaluate the performance of the trained model on clean and poisoned samples.

        Parameters:
        - clean_test (Tuple[np.ndarray, np.ndarray]): Clean test images and labels.
        - poisoned_test (Tuple[np.ndarray, np.ndarray]): Poisoned test images and labels.
        - model_poisoned (tf.keras.Model): The trained model with poisoned data.

        Returns:
        - Tuple: Contains the following elements:
            - score_clean (Tuple[float, float]): Loss and accuracy on clean test data.
            - score_poisoned (Tuple[float, float]): Loss and accuracy on poisoned test data.
        """
        # Retrieve attack scores
        print(f"[{TAG}] Retrieve attack scores")
        score_clean = attack_metrics[0]
        score_poisoned = attack_metrics[1]
        
        # Comparing test losses
        print(f"[{TAG}] Comparing test losses")
        print(f"Test loss on clean data: {score_clean[0]:.2f} "
            f"vs test loss on poisoned data: {score_poisoned[0]:.2f}")

        # Comparing test accuracies
        print(f"[{TAG}] Comparing test accuracies")
        print(f"Test accuracy on clean data: {score_clean[1]:.2f} "
            f"vs test accuracy on poisoned data: {score_poisoned[1]:.2f}")

        # Retrieve defense scores
        print(f"[{TAG}] Retrieve defense scores")
        confusion_matrix = defense_metrics[0]
        sprites_by_class = defense_metrics[1]
        
        # Displaying the reported defense effectiveness
        print(f"[{TAG}] Displaying the reported defense effectiveness")
        jsonObject_matrix = json.loads(s=confusion_matrix)
        for label in jsonObject_matrix:
            print(label)
            pprint.pprint(jsonObject_matrix[label])
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "confusion_matrix": json.loads(s=confusion_matrix),
            "sprites_by_class": sprites_by_class,
            "test_metrics": {
                "loss": {
                    "clean_data": f"{score_clean[0]:.2f}",
                    "poisoned_data": f"{score_poisoned[0]:.2f}"
                },
                "accuracy": {
                    "clean_data": f"{score_clean[1]:.2f}",
                    "poisoned_data": f"{score_poisoned[1]:.2f}"
                }
            },
            "params": self.params,
            "summary": summary
        }

        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
