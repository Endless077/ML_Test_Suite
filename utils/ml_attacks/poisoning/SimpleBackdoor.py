# CleanLabelBackdoor & SimpleBackdoor ART Class
from art.attacks.poisoning import PoisoningAttackCleanLabelBackdoor, PoisoningAttackBackdoor
from art.attacks.poisoning.perturbations import add_pattern_bd
from art.utils import to_categorical

# Support
import numpy as np

# Own Modules
from classes.AttackClass import BackdoorAttack

# Utils
from utils.model import *

'''
Implementation of backdoor attacks introduced in Gu et al., 2017.
Applies a number of backdoor perturbation functions and switches label to target label.

Paper link: https://arxiv.org/abs/1708.06733
'''

TAG = "SimpleBackdoor"

class SimpleBackdoor(BackdoorAttack):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)

    def perform_attack(self, target_lbl=[]):
        # Defining a poisoning backdoor attack
        print(f"[{TAG}] Defining a poisoning backdoor attack")
        backdoor_attack = PoisoningAttackBackdoor(
            # A single perturbation function or list of perturbation functions that modify input.
            perturbation=add_pattern_bd
            )
        
        poisoned_percentage = self.params["poisoned_percentage"]
        print(f"[{TAG}] Poisoned Percentage: {poisoned_percentage * 100}%")
        
        # Defining target random labels
        print(f"[{TAG}] Defining target random labels")
        num_classes = self.dataset_stats["num_classes"]
        if target_lbl is not None and len(target_lbl) > 0:
            # Convert target_lbl to a numpy array for easier manipulation
            if not isinstance(target_lbl, np.ndarray):
                target_lbl = np.array(target_lbl)
            
            # Remove values outside the range [0, num_classes - 1]
            target_lbl = target_lbl[(target_lbl >= 0) & (target_lbl < num_classes)]
            
            # Limit the number of labels to num_classes - 1
            if len(target_lbl) > num_classes - 1:
                target_lbl = target_lbl[:num_classes - 1]
        else:
            target_lbl = np.random.permutation(num_classes)
             
        target_labels = target_lbl
        print(f"[{TAG}] Target labels:\n {target_labels}")
        
        # Poisoning the training data
        print(f"[{TAG}] Poisoning the training data")
        (is_poison_train, train_images, train_labels) = self.poison_dataset(
            clean_images=self.dataset_struct["train_data"][0],
            clean_labels=self.dataset_struct["train_data"][1],
            target_labels=target_labels,
            backdoor_attack=backdoor_attack,
            poisoned_percentage=poisoned_percentage)

        # Poisoning the test data
        print(f"[{TAG}] Poisoning the test data")
        (is_poison_test, test_images, test_labels) = self.poison_dataset(
            clean_images=self.dataset_struct["test_data"][0],
            clean_labels=self.dataset_struct["test_data"][1],
            target_labels=target_labels,
            backdoor_attack=backdoor_attack,
            poisoned_percentage=poisoned_percentage)

        # Getting the clean and poisoned images & labels from the test set
        print(f"[{TAG}] Getting the clean and poisoned images & labels from the test set")
        clean_test_images, clean_test_labels = test_images[is_poison_test == 0], test_labels[is_poison_test == 0]
        poisoned_test_images, poisoned_test_labels = test_images[is_poison_test == 1], test_labels[is_poison_test == 1]
        
        # Shuffling the training data
        print(f"[{TAG}] Shuffling the training data")
        num_train = train_images.shape[0]
        shuffled_indices = np.arange(num_train)
        np.random.shuffle(shuffled_indices)
        is_poison_train = is_poison_train[shuffled_indices]
        train_images = train_images[shuffled_indices]
        train_labels = train_labels[shuffled_indices]
        
        # Creating and training a victim classifier with the poisoned data
        print(f"[{TAG}] Creating and training a victim classifier with the poisoned data")
        model_poisoned = fit_model((train_images, train_labels), None, copy_model(self.model), self.params["batch_size"], self.params["epochs"])
        
        print(f"[{TAG}] Returning all the results")
        return (clean_test_images, clean_test_labels), (poisoned_test_images, poisoned_test_labels), (is_poison_train, is_poison_test, shuffled_indices), model_poisoned
    
    def evaluate_prediction(self, clean_test_images, poisoned_test_images, model_poisoned, num_samples=3):
        # Getting predictions for the selected images
        print(f"[{TAG}] Getting predictions for the selected images")
        clean_predictions = model_poisoned.predict(x=clean_test_images)

        # Getting random ten images from the poisoned test set
        print(f"[{TAG}] Getting random ten images from the poisoned test set")
        sample_indices = np.random.choice(
            a=len(poisoned_test_images),
            size=num_samples
            )
        
        sample_poisoned_images = poisoned_test_images[sample_indices]
        
        return clean_predictions, sample_poisoned_images
        
    def evaluate(self, clean_test, poisoned_test, model_poisoned):
        # Evaluating the performance of the vulnerable classifier on clean and poisoned samples
        print(f"[{TAG}] Evaluating the performance of the vulnerable classifier on clean and poisoned samples")
        score_clean = model_poisoned.evaluate(x=clean_test[0], y=clean_test[1])
        score_poisoned = model_poisoned.evaluate(x=poisoned_test[0], y=poisoned_test[1])

        return score_clean, score_poisoned
    
    def plotting_stats(self):
        raise NotImplementedError

    def result(self, score_clean, score_poisoned, poison_data):
        # Comparing test losses
        print(f"Clean test set loss: {score_clean[0]:.2f} "
            f"vs poisoned set test loss: {score_poisoned[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test set accuracy: {score_clean[1]:.2f} "
            f"vs poisoned test set accuracy: {score_poisoned[1]:.2f}")
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary_clean_model = summary_model(self.model)
        summary_poisoned_model = summary_model(poison_data["model_poisoned"])
        
        result_dict = {
            "clean_scores": {
                "loss": f"{score_clean[0]:.2f}",
                "accuracy": f"{score_clean[1]:.2f}"
            },
            "poisoned_scores": {
                "loss": f"{score_poisoned[0]:.2f}",
                "accuracy": f"{score_poisoned[1]:.2f}"
            },
            "summary_clean_model": summary_clean_model,
            "summary_poisoned_model": summary_poisoned_model,
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
