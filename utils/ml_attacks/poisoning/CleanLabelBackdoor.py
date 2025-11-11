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

TAG = "CleanLabelBackdoor"

class CleanLabelBackdoor(BackdoorAttack):
    """
    Clean Label Backdoor attack class.

    This class implements a backdoor attack by poisoning the training and test data with perturbations
    and target labels. The attack utilizes a pattern-based perturbation functions and does not change labels.

    Paper: https://people.csail.mit.edu/madry/lab/cleanlabel.pdf
    """
    def __init__(self, model, dataset_struct, dataset_stats, params):
        """
        Initialize the Clean Label Backdoor attack instance.

        Parameters:
        - model (tf.keras.Model): The Keras model to attack.
        - dataset_struct (Dict[str, tf.Tensor]): Dictionary containing training and test data.
        - dataset_stats (Dict[str, Any]): Dictionary containing dataset statistics.
        - params (Dict[str, Any]): Dictionary containing parameters for the attack.
        """
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def perform_attack(self, target_lbl=[]):
        """
        Perform the backdoor attack by poisoning the dataset with specific patterns and target labels.

        Parameters:
        - target_lbl (List[int], optional): List of target labels to assign for backdoor samples. If None,
          target labels will be chosen randomly. Defaults to None.

        Returns:
        - Tuple: Contains the following elements:
            - clean_test_images (np.ndarray): Clean test images.
            - clean_test_labels (np.ndarray): Clean test labels.
            - poisoned_test_images (np.ndarray): Poisoned test images.
            - poisoned_test_labels (np.ndarray): Poisoned test labels.
            - is_poison_train (np.ndarray): Array indicating which training samples are poisoned.
            - is_poison_test (np.ndarray): Array indicating which test samples are poisoned.
            - shuffled_indices (np.ndarray): Shuffled indices for training data.
            - model_poisoned (tf.keras.Model): The trained model with poisoned data.
        """
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        print(f"[{TAG}] Creating a classifier by wrapping our TF model in ART's KerasClassifier class")
        classifier = self.create_keras_classifier(self.model)

        # Defining a poisoning backdoor attack
        print(f"[{TAG}] Defining a poisoning backdoor attack")
        backdoor_attack = PoisoningAttackBackdoor(
            # A single perturbation function or list of perturbation functions that modify input.
            perturbation=add_pattern_bd
            )
        
        poisoned_percentage = self.params["poisoned_percentage"]
        print(f"[{TAG}] Poisoned Percentage: {poisoned_percentage * 100}%")
        
        # Defining a target label for poisoning
        print(f"[{TAG}] Defining a target label for poisoning")
        num_classes = self.dataset_stats["num_classes"]
        target_label = target_lbl[0] if target_lbl else np.random.randint(0, num_classes)
        
        target = to_categorical(
            labels=np.array([target_label], dtype=int),
            nb_classes=num_classes
        )[0]
        
        print(f"[{TAG}] Target label (numpy array):\n {target_label}")
        print(f"[{TAG}] Target label (categorical):\n {target}")
        
        # Defining a clean label backdoor attack
        print(f"[{TAG}] Defining a clean label backdoor attack")
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
        print(f"[{TAG}] Poisoning the training data")
        (is_poison_train, train_images, train_labels) = self.poison_dataset(
            clean_images=self.dataset_struct["train_data"][0],
            clean_labels=self.dataset_struct["train_data"][1],
            target_labels=[target_label],
            backdoor_attack=backdoor_attack,
            poisoned_percentage=poisoned_percentage)

        # Poisoning the test data
        print(f"[{TAG}] Poisoning the test data")
        (is_poison_test, test_images, test_labels) = self.poison_dataset(
            clean_images=self.dataset_struct["test_data"][0],
            clean_labels=self.dataset_struct["test_data"][1],
            target_labels=[target_label],
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
        model_poisoned = fit_model((train_images, train_labels), copy_model(self.model), self.params["batch_size"], self.params["epochs"])
        
        print(f"[{TAG}] Returning all the results")
        return (clean_test_images, clean_test_labels), (poisoned_test_images, poisoned_test_labels), (is_poison_train, is_poison_test, shuffled_indices), model_poisoned
        
    def evaluate(self, clean_test, poisoned_test, model_poisoned):
        """
        Evaluate the performance of the trained model on clean and poisoned test data.

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

        return score_clean, score_poisoned

    def plotting_stats(self):
        """
        This method is not implemented. It should handle plotting statistics if required.

        Raises:
        - NotImplementedError: This method has not been implemented yet.
        """
        raise NotImplementedError

    def result(self, score_clean, score_poisoned, poison_data):
        """
        Print and save the results of the attack, including performance metrics.

        Parameters:
        - score_clean (Tuple[float, float]): Loss and accuracy on clean test data.
        - score_poisoned (Tuple[float, float]): Loss and accuracy on poisoned test data.
        - poison_data (Tuple[np.ndarray, np.ndarray]): The poisoned images and their labels.

        Returns:
        - Dict[str, Any]: A dictionary containing the results of the attack.
        """
        # Comparing test losses
        print(f"Clean test set loss: {score_clean[0]:.2f} "
            f"vs poisoned set test loss: {score_poisoned[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test set accuracy: {score_clean[1]:.2f} "
            f"vs poisoned test set accuracy: {score_poisoned[1]:.2f}")
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "clean_scores": {
                "loss": f"{score_clean[0]:.2f}",
                "accuracy": f"{score_clean[1]:.2f}"
            },
            "poisoned_scores": {
                "loss": f"{score_poisoned[0]:.2f}",
                "accuracy": f"{score_poisoned[1]:.2f}"
            },
            "params": self.params,
            "summary": summary
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
