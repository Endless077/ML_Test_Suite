# STRIP ART Class
from art.defences.transformer.poisoning import STRIP

# Support
import numpy as np

# Own Modules
from ml_attacks.poisoning.CleanLabelBackdoor import CleanLabelBackdoor
from ml_attacks.poisoning.SimpleBackdoor import SimpleBackdoor
from classes.DefenseClass import TransformerDefense

# Utils
from utils.model import *

TAG = "STRongIntentionalPerturbation"

class STRongIntentionalPerturbation(TransformerDefense):
    """
    STRIP Defense against Trojan attacks on deep neural networks (Gao et al., 2020).

    This class implements the STRIP (Strongly Intentional Perturbation) defense against Trojan attacks.
    The defense is designed to mitigate the effects of poison attacks on neural networks.

    Paper: https://arxiv.org/abs/1902.06531
    """
    def __init__(self, model, dataset_struct, dataset_stats, params):
        """
        Initialize the STRIP defense instance.

        Parameters:
        - model (tf.keras.Model): The Keras model to defend.
        - dataset_struct (Dict[str, tf.Tensor]): Dictionary containing training and test data.
        - dataset_stats (Dict[str, Any]): Dictionary containing dataset statistics.
        - params (Dict[str, Any]): Dictionary containing parameters for the defense.
        """
        super().__init__(model, dataset_struct, dataset_stats, params)

    def perform_defense(self):
        """
        Perform the STRIP defense by applying a poison attack and wrapping the model with STRIP.

        Returns:
        - Tuple[Tuple[np.ndarray, np.ndarray], np.ndarray, Any, STRIP]: 
          - Clean and poisoned test data.
          - Poisoned model.
          - STRIP defense instance.
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
        
        clean_test, poisoned_test, poison_struct, model_poisoned = backdoor_attack.perform_attack(target_lbl=target_labels)
        
        # Evaluating the performance of the vulnerable classifier on clean and poisoned images
        #print(f"[{TAG}] Evaluating the performance of the vulnerable classifier on clean and poisoned images")
        #backdoor_attack.evaluate(clean_test, poisoned_test, model_poisoned)
        
        # Wrapping the model in KerasClassifier
        print(f"[{TAG}] Wrapping the model in KerasClassifier")
        classifier_poisoned = self.create_keras_classifier(model_poisoned)
        
        # Initializing the defense object
        print(f"[{TAG}] Initializing the defense object")
        strip = STRIP(classifier=classifier_poisoned)

        # Creating a STRIP defense
        print(f"[{TAG}] Creating a STRIP defense")
        defense = strip()

        # Mitigating the effect of the poison
        print(f"[{TAG}] Mitigating the effect of the poison")
        defense.mitigate(x_val=clean_test[0][:len(clean_test[0])//2]) 
        
        return clean_test, poisoned_test, model_poisoned, defense
    
    def evaluate(self, clean_test, poisoned_test, model_poisoned, defense):
        """
        Evaluate the defense performance on clean and poisoned test samples.

        Parameters:
        - clean_test (Tuple[np.ndarray, np.ndarray]): Clean test data.
        - poisoned_test (Tuple[np.ndarray, np.ndarray]): Poisoned test data.
        - model_poisoned (tf.keras.Model): The model that has been poisoned.
        - defense (STRIP): The STRIP defense instance.

        Returns:
        - Tuple[Tuple[int, int], int, int]:
          - Number of abstained predictions on clean and poisoned samples.
          - Total number of clean and poisoned predictions.
        """
        # Obtaining predictions for clean and poisoned samples
        print(f"[{TAG}] Obtaining predictions for clean and poisoned samples")
        clean_preds = defense.predict(x=clean_test[0][len(clean_test[0])//2:])
        poison_preds = defense.predict(x=poisoned_test[0])

        # Getting the number of predictions that have been abstained
        print(f"[{TAG}] Getting the number of predictions that have been abstained")
        num_abstained_clean = np.sum(np.all(a=(clean_preds == np.zeros(10)), axis=1))
        num_abstained_poison = np.sum(np.all(a=(poison_preds == np.zeros(10)), axis=1))

        # Getting the total number of poisoned and clean predictions
        print(f"[{TAG}] Getting the total number of poisoned and clean predictions")
        num_clean = len(clean_preds)
        num_poison = len(poison_preds)
        
        return (num_abstained_clean, num_abstained_poison), num_clean, num_poison

    def plotting_stats(self):
        """
        This method is not implemented. It should handle plotting statistics if required.

        Raises:
        - NotImplementedError: This method has not been implemented yet.
        """
        raise NotImplementedError
    
    def result(self, num_abstained, num_clean, num_poison):
        """
        Print and save the results of the defense evaluation.

        Parameters:
        - num_abstained (Tuple[int, int]): Number of abstained predictions for clean and poisoned samples.
        - num_clean (int): Total number of clean predictions.
        - num_poison (int): Total number of poisoned predictions.

        Returns:
        - result_dict (Dict[str, Any]): Dictionary containing the results of the defense.
        """
        # Calculating and displaying the ratio of abstained samples
        print(f"[{TAG}] Calculating and displaying the ratio of abstained samples")
        print(f"Abstained {num_abstained[0]}/{num_clean} clean samples ({round(num_abstained[0] / float(num_clean) * 100, 2)}% FP rate)")
        print(f"Abstained {num_abstained[1]}/{num_poison} poison samples ({round(num_abstained[1] / float(num_poison)* 100, 2)}% TP rate)")
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "clean_samples": {
                "abstanied": f"{num_abstained[0]}/{num_clean}",
                "fp_rate": f"{round(num_abstained[0] / float(num_clean) * 100, 2)}",
            },
            "poison_samples": {
                "abstanied": f"{num_abstained[1]}/{num_poison}",
                "tp_rate": f"{round(num_abstained[1] / float(num_poison)* 100, 2)}",
            },
            "params": self.params,
            "summary": summary,
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
