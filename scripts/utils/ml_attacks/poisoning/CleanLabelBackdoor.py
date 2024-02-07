# Import Modules
import numpy as np
from art.attacks.poisoning import PoisoningAttackCleanLabelBackdoor, PoisoningAttackBackdoor
from art.attacks.poisoning.perturbations import add_pattern_bd
from art.utils import to_categorical

# Own Modules
from utils.model import copy_model, compile_model
from classes.AttackClass import AttackClass, BackdoorAttack

'''
Implementation of Clean-Label Backdoor Attack introduced in Turner et al., 2018.
Applies a number of backdoor perturbation functions and does not change labels.

Paper link: https://people.csail.mit.edu/madry/lab/cleanlabel.pdf
'''

class CleanLabelBackdoor(BackdoorAttack):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def perform_attack(self, model, target_lbl=None, percent_poison=0.3):
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        classifier = self.create_keras_classifier(model)

        # Defining a poisoning backdoor attack
        backdoor_attack = PoisoningAttackBackdoor(
            # A single perturbation function or list of perturbation functions that modify input.
            perturbation=add_pattern_bd
            )
        
        # Defining a target label for poisoning
        if(target_lbl is None):
            num_classes = self.dataset_stats["num_classes"]
            num_labels = np.random.randint(1, num_classes - 1)
            target_labels = np.random.sample(range(num_classes), num_labels)
            
            target = to_categorical(
                labels=target_labels,
                nb_classes=num_classes
                )[0]
        else:
            target = to_categorical(
                labels=target_lbl,
                nb_classes=num_classes
                )[0]

        # Defining a clean label backdoor attack
        backdoor_attack = PoisoningAttackCleanLabelBackdoor(
            backdoor=backdoor_attack,           # The backdoor chosen for this attack
            proxy_classifier=classifier,        # The classifier for this attack ideally it solves the same or similar classification task as the original classifier (default: CLASSIFIER_LOSS_GRADIENTS_TYPE)
            target=target,                      # The target label to poison
            pp_poison=0.33,                     # The percentage of the data to poison. Note: Only data within the target label is poisoned (default: 0.33)
            norm=2,                             # The norm of the adversarial perturbation supporting “inf”, np.inf, 1 or 2
            eps=0.3,                            # Maximum perturbation that the attacker can introduce (default 0.3)
            eps_step=0.1,                       # Attack step size (input variation) at each iteration (default: 0.1)
            max_iter=100,                       # The maximum number of iterations (default: 100)
            num_random_init=0                   # Number of random initializations within the epsilon ball. For num_random_init=0 starting at the original input (default: 0)
            )

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
        model_poisoned = copy_model(model)
        model_poisoned.fit(
            x=train_images,
            y=train_labels,
            epochs=self.params["epochs"]
            )
        
        return (clean_test_images, clean_test_labels), (poisoned_test_images, poisoned_test_labels), (is_poison_train, is_poison_test, shuffled_indices), model_poisoned
        
    def evaluate(self, clean_test, poisoned_test, model_poisoned):
        # Evaluating the performance of the vulnerable classifier on clean and poisoned samples
        score_clean = model_poisoned.evaluate(x=clean_test[0], y=clean_test[1])
        score_poisoned = model_poisoned.evaluate(x=poisoned_test[0], y=poisoned_test[1])

        return score_clean, score_poisoned
    
    def print_stats(self, score_clean, score_poisoned):
        # Comparing test losses
        print("------ TEST METRICS OF POISONED MODEL ------")
        print(f"Test loss on clean data: {score_clean[0]:.2f} "
            f"vs test loss on poisoned data: {score_poisoned[0]:.2f}")

        # Comparing test losses
        print(f"Test accuracy on clean data: {score_clean[1]:.2f} "
            f"vs test accuracy on poisoned data: {score_poisoned[1]:.2f}")

    def plotting_stats(self):
        pass
