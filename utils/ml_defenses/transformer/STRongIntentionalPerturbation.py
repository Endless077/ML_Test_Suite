# STRIP ART Class
from art.defences.transformer.poisoning import STRIP

# Support
import numpy as np

# Own Modules
from ml_attacks.poisoning.CleanLabelBackdoor import CleanLabelBackdoor
from ml_attacks.poisoning.SimpleBackdoor import SimpleBackdoor
from classes.DefenseClass import DefenseClass, TransformerDefense

# Utils
from utils.model import *

'''
Implementation of STRIP: A Defence Against Trojan Attacks on Deep Neural Networks (Gao et. al. 2020)

Paper link: https://arxiv.org/abs/1902.06531
'''

TAG = "STRongIntentionalPerturbation"

class STRongIntentionalPerturbation(TransformerDefense):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats)

    def perform_defense(self):
        # Defining new target labels (all 9s)
        num_classes = self.dataset_stats["num_classes"]
        random_label = np.random.randint(0, num_classes)
        
        target_labels = np.array([random_label] * num_classes)

        attack = self.params["poison_attack"]
        attack_params = self.params["poison_params"]
        if(attack.lower() == "cleanlabels"):
            # Defining a clean label backdoor attack
            #backdoor_class = CleanLabelBackdoor(model=self.vulnerable_model,
            #                                    dataset_struct=self.dataset_struct,
            #                                    dataset_stats=self.dataset_stats,
            #                                    params=attack_params)
            backdoor_attack = CleanLabelBackdoor(model=self.robust_model,
                                                dataset_struct=self.dataset_struct,
                                                dataset_stats=self.dataset_stats,
                                                params=attack_params)
        elif(attack.lower() == "simple"):
            # Defining a poisoning backdoor attack
            #backdoor_class = SimpleBackdoor(model=self.vulnerable_model,
            #                                    dataset_struct=self.dataset_struct,
            #                                    dataset_stats=self.dataset_stats,
            #                                    params=attack_params)
            backdoor_attack = SimpleBackdoor(model=self.robust_model,
                                             dataset_struct=self.dataset_struct,
                                             dataset_stats=self.dataset_stats,
                                             params=attack_params)
        else:
            #backdoor_class = None
            backdoor_attack = None
        
        clean_test, poisoned_test, model_poisoned = backdoor_attack.perform_attack(model=self.robust_model, target_lbl=target_labels)
        
        # Evaluating the performance of the vulnerable classifier on clean and poisoned images
        #backdoor_attack.evaluate(clean_test, poisoned_test, model_poisoned)
        
        # Wrapping the model in KerasClassifier
        classifier_poisoned = self.create_keras_classifier(model_poisoned)
        
        # Initializing the defense object
        strip = STRIP(classifier=classifier_poisoned)

        # Creating a STRIP defense
        defense = strip()

        # Mitigating the effect of the poison 
        defense.mitigate(x_val=clean_test[0][:len(clean_test[0])//2]) 
        
        return clean_test, poisoned_test, model_poisoned, defense
    
    def evaluate(self, clean_test, poisoned_test, model_poisoned, defense):
        # Obtaining predictions for clean and poisoned samples
        clean_preds = defense.predict(x=clean_test[0][len(clean_test[0])//2:])
        poison_preds = defense.predict(x=poisoned_test[0])

        # Getting the number of predictions that have been abstained
        num_abstained_clean = np.sum(np.all(a=(clean_preds == np.zeros(10)), axis=1))
        num_abstained_poison = np.sum(np.all(a=(poison_preds == np.zeros(10)), axis=1))

        # Getting the total number of poisoned and clean predictions
        num_clean = len(clean_preds)
        num_poison = len(poison_preds)
        
        return (num_abstained_clean, num_abstained_poison), num_clean, num_poison

    def plotting_stats(self):
        raise NotImplementedError
    
    def result(self, num_abstained, num_clean, num_poison):
        # Calculating and displaying the ratio of abstained samples
        print(f"Abstained {num_abstained[0]}/{num_clean} clean samples ({round(num_abstained[0] / float(num_clean) * 100, 2)}% FP rate)")
        print(f"Abstained {num_abstained[1]}/{num_poison} poison samples ({round(num_abstained[1] / float(num_poison)* 100, 2)}% TP rate)")
        
        # Build summary model and result
        vulnerable_model_summary_dict = summary_model(self.vulnerable_model)
        robust_model_summary_dict = summary_model(self.robust_model)
        
        result_dict = {
            "clean_samples": {
                "abstanied": f"{num_abstained[0]}/{num_clean}",
                "fp_rate": f"{round(num_abstained[0] / float(num_clean) * 100, 2)}",
            },
            "poison_samples": {
                "abstanied": f"{num_abstained[1]}/{num_poison}",
                "tp_rate": f"{round(num_abstained[1] / float(num_poison)* 100, 2)}",
            },
            "robust_model_summary_dict": robust_model_summary_dict,
            "vulnerable_model_summary_dict": vulnerable_model_summary_dict
        }
        
        # Save Summary File
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
