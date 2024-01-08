# Import Modules
import numpy as np
from art.attacks.poisoning import PoisoningAttackBackdoor
from art.attacks.poisoning.perturbations import add_pattern_bd
from art.estimators.classification import KerasClassifier
from art.utils import to_categorical

# Own Modules
from utils.model import copy_model, compile_model
from classes.AttackClass import AttackClass, BackdoorAttack

'''
Implementation of backdoor attacks introduced in Gu et al., 2017.
Applies a number of backdoor perturbation functions and switches label to target label.

Paper link: https://arxiv.org/abs/1708.06733
'''

class SimpleBackdoor(BackdoorAttack):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)

    def perform_attack(self, model, target_lbl=None, percent_poison=0.3):
        # Defining a poisoning backdoor attack
        backdoor_attack = PoisoningAttackBackdoor(
            # A single perturbation function or list of perturbation functions that modify input.
            perturbation=add_pattern_bd
            )
        
        # Defining target random lables
        if(target_lbl is None):
            target_labels = np.random.permutation(self.dataset_stats["num_classes"])
        else:
            target_labels = target_lbl
        
        # Poisoning the training data
        (is_poison_train, train_images, train_labels) = self.poison_dataset(
            clean_images=self.dataset_struct["train_data"][0],
            clean_labels=self.dataset_struct["train_data"][1],
            target_labels=target_labels,
            backdoor_attack=backdoor_attack,
            percent_poison=percent_poison)

        # Poisoning the test data
        (is_poison_test, test_images, test_labels) = self.poison_dataset(
            clean_images=self.dataset_struct["test_data"][0],
            clean_labels=self.dataset_struct["test_data"][1],
            target_labels=target_labels,
            backdoor_attack=backdoor_attack,
            percent_poison=percent_poison)

        # Getting the clean and poisoned images & labels from the test set
        clean_test_images, clean_test_labels = test_images[is_poison_test == 0], test_labels[is_poison_test == 0]
        poisoned_test_images, poisoned_test_labels = test_images[is_poison_test == 1], test_labels[is_poison_test == 1]
        
        # Shuffling the training data
        num_train = train_images.shape[0]
        shuffled_indices = np.arange(num_train)
        np.random.shuffle(shuffled_indices)
        train_images = train_images[shuffled_indices]
        train_labels = train_labels[shuffled_indices]
        
        # Creating and training a victim classifier
        # with the poisoned data
        model_poisoned = copy_model(self.model)
        model_poisoned = compile_model(model_poisoned)
        model_poisoned.fit(
            x=train_images,
            y=train_labels,
            epochs=self.params["epochs"]
            )
        
        return (clean_test_images, clean_test_labels), (poisoned_test_images, poisoned_test_labels), model_poisoned
    
    def evaluate_prediction(self, clean_test_images, poisoned_test_images, model_poisoned, num_samples=3):
        # Getting predictions for the selected images
        clean_predictions = model_poisoned.predict(x=clean_test_images)

        # Getting random ten images from the poisoned test set
        sample_indices = np.random.choice(
            a=len(poisoned_test_images),
            size=num_samples
            )
        sample_poisoned_images = poisoned_test_images[sample_indices]
        
        return clean_predictions, sample_poisoned_images
        
    def evaluate(self, clean_test, poisoned_test, model_poisoned):
        # Evaluating the performance of the vulnerable classifier on clean and poisoned samples
        score_clean = model_poisoned.evaluate(x=clean_test[0], y=clean_test[1])
        score_poisoned = model_poisoned.evaluate(x=poisoned_test[0], y=poisoned_test[1])

        return score_clean, score_poisoned
    
    def print_stats(self, scores_clean, scores_adv):
        # Comparing test losses
        print("------ TEST METRICS OF POISONED MODEL ------")
        print(f"Test loss on clean data: {score_clean[0]:.2f} "
            f"vs test loss on poisoned data: {score_poisoned[0]:.2f}")

        # Comparing test losses
        print(f"Test accuracy on clean data: {score_clean[1]:.2f} "
            f"vs test accuracy on poisoned data: {score_poisoned[1]:.2f}")
    
    def plotting_stats(self, scores_clean, scores_adv):
        pass
