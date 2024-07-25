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

'''
Method from Chen et al., 2018 performing poisoning detection based on activations clustering.

Paper link: https://arxiv.org/abs/1811.03728
Please keep in mind the limitations of defences. For more information on the limitations of this defence, see https://arxiv.org/abs/1905.13409 . For details on how to evaluate classifier security in general, see https://arxiv.org/abs/1902.06705
'''

TAG = "ActivationDefense"

class ActivationDefense(TransformerDefense):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
        
    def perform_defense(self):
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
            reduce=self.params["reduce"],
            nb_dims=self.params["nb_dims"],
            cluster_analysis=self.params["nb_dims"]
            )
        
        return clean_test, poisoned_test, is_poisoned_stats, model_poisoned, (report, is_clean_reported), defense
    
    def evaluate_report(self, report_stats, is_poisoned_stats, defense):
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
        # Evaluating the performance of the vulnerable classifier on clean and poisoned samples
        print(f"[{TAG}] Evaluating the performance of the vulnerable classifier on clean and poisoned samples")
        score_clean = model_poisoned.evaluate(x=clean_test[0], y=clean_test[1])
        score_poisoned = model_poisoned.evaluate(x=poisoned_test[0], y=poisoned_test[1])
        
        return (score_clean, score_poisoned)
    
    def evaluate(self, clean_test, poisoned_test, is_poisoned_stats, model_poisoned, report_stats, defense):
        # Evaluate attack metrics
        print(f"[{TAG}] Evaluate attack metrics")
        attack_metrics = self.evaluate_metrics(clean_test, poisoned_test, model_poisoned)
        
        # Evaluate defense metrics
        print(f"[{TAG}] Evaluate defense metrics")
        defense_metrics = self.evaluate_report(report_stats, is_poisoned_stats, defense)
        
        return attack_metrics, defense_metrics
            
    def plotting_stats(self):
        raise NotImplementedError
    
    def result(self, attack_metrics, defense_metrics):
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
            "summary": summary
        }

        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
