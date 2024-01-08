# Import Modules
import numpy as np
from art.attacks.poisoning import PoisoningAttackBackdoor
from art.attacks.poisoning import PoisoningAttackCleanLabelBackdoor
from art.defences.detector.poison import ActivationDefence
from art.estimators.classification import KerasClassifier
from art.utils import to_categorical

# Own Modules
from classes.DefenseClass import DefenseClass, TransformerDefense
from ml_attacks.poisioning.CleanLabelBackdoor import CleanLabelBackdoor
from ml_attacks.poisioning.SimpleBackdoor import SimpleBackdoor

'''
Method from Chen et al., 2018 performing poisoning detection based on activations clustering.

Paper link: https://arxiv.org/abs/1811.03728
Please keep in mind the limitations of defences. For more information on the limitations of this defence, see https://arxiv.org/abs/1905.13409 . For details on how to evaluate classifier security in general, see https://arxiv.org/abs/1902.06705
'''

class ActivationDefence(TransformerDefense):
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
        
        classifier: CLASSIFIER_NEURALNETWORK_TYPE
        x_train: ndarray
        y_train: ndarray
        generator: DataGenerator | None = None
        ex_re_threshold: float | None = None
        
        # Initializing a defense object
        defense = ActivationDefence(
            classifier=classifier_poisoned,     # The classifier on which to apply the defense
            x_train=train_images,               # The training images
            y_train=train_labels,               # The training labels
            generator=None,                     # A DataGenerator object (default: None)
            ex_re_threshold=None                # A threshold fload (default: None)
            )
        
        # Detecting poisoned samples in the provided images
        report, is_clean_reported = defense.detect_poison(
            nb_clusters=2,
            reduce="PCA",
            nb_dims=10)
        
        return report, is_clean_reported, defence
    
    def evaluate(self, report, is_clean_reported):
        # Inverting our poison indicator array
        # so that clean samples are indicated as "True" (1)
        # and poisoned samples as "False" (0)
        is_clean = (is_poison_train == 0)
        
        # Generating a confusion matrix to evaluate defenses
        confusion_matrix = defense.evaluate_defence(is_clean=is_clean[shuffled_indices])

        return confusion_matrix
    
    def print_stats(self, num_abstained, num_clean, num_poison):
        pass

    def plotting_stats(self):
        pass