# Import Modules
import numpy as np
from art.attacks.poisoning import PoisoningAttackBackdoor
from art.attacks.poisoning import PoisoningAttackCleanLabelBackdoor
from art.defences.transformer.poisoning import STRIP
from art.estimators.classification import KerasClassifier
from art.utils import to_categorical

# Own Modules
from classes.DefenseClass import DefenseClass, TransformerDefense
from ml_attacks.poisioning.CleanLabelBackdoor import CleanLabelBackdoor
from ml_attacks.poisioning.SimpleBackdoor import SimpleBackdoor

'''
Implementation of STRIP: A Defence Against Trojan Attacks on Deep Neural Networks (Gao et. al. 2020)

Paper link: https://arxiv.org/abs/1902.06531
'''

class STRongIntentionalPerturbation(TransformerDefense):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)

    def perform_defense(self, percent_poison=0.3):
        # Defining new target labels (all 9s)
        num_classes = self.dataset_stats["num_classes"]
        random_label = np.random.randint(0, num_classes)
        
        target_labels = np.array([random_label] * num_classes)

        attack = params["method"].split(':')[1].strip()
        if(attack.lower() == "cleanlabels"):
            # Defining a clean label backdoor attack
            #backdoor_class = CleanLabelBackdoor(model=self.vulnerable_model)
            backdoor_attack = CleanLabelBackdoor(model=self.robust_model)
        elif(attack.lower() == "simple"):
            # Defining a poisoning backdoor attack
            #backdoor_class = SimpleBackdoor(model=self.vulnerable_model)
            backdoor_attack = SimpleBackdoor(model=self.robust_model)
        else:
            backdoor_class = None
            backdoor_attack = None
        
        clean_test, poisioned_test, model_poisoned = backdoor_attack.perform_attack(model=self.robust_model, target_lbl=target_labels, percent_poison=percent_poison)
        
        # Evaluating the performance of the vulnerable classifier on clean and poisoned images
        #backdoor_attack.evaluate(clean_test, poisioned_test, model_poisoned)
        
        # Wrapping the model in KerasClassifier
        classifier_poisoned = self.create_keras_classifier(model_poisoned)
        
        # Initializing the defense object
        strip = STRIP(classifier=classifier_poisoned)

        # Creating a STRIP defense
        defense = strip()

        # Mitigating the effect of the poison 
        defense.mitigate(x_val=clean_test[0][:len(clean_test[0])//2]) 
        
        return clean_test, poisioned_test, model_poisoned, defense
    
    def evaluate(self, clean_test, poisioned_test, model_poisoned, defense):
        # Obtaining predictions for clean and poisoned samples
        poison_preds = defense.predict(x=poisoned_test[0])
        clean_preds = defense.predict(x=clean_test[0][len(clean_test[0])//2:])

        # Getting the number of predictions that have been abstained
        num_abstained_clean = np.sum(np.all(a=(clean_preds == np.zeros(10)), axis=1))
        num_abstained_poison = np.sum(np.all(a=(poison_preds == np.zeros(10)), axis=1))

        # Getting the total number of poisoned and clean predictions
        num_clean = len(clean_preds)
        num_poison = len(poison_preds)
        
        return (num_abstained_clean, num_abstained_poison), num_clean, num_poison
    
    def print_stats(self, num_abstained, num_clean, num_poison):
        # Calculating and displaying the ratio of abstained samples
        print(f"Abstained {num_abstained_poison}/{num_poison} poison samples ({round(num_abstained_poison / float(num_poison)* 100, 2)}% TP rate)")
        print(f"Abstained {num_abstained_clean}/{num_clean} clean samples ({round(num_abstained_clean / float(num_clean) * 100, 2)}% FP rate)")


    def plotting_stats(self):
        pass