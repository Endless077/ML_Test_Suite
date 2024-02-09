# Import Modules
import numpy as np
from art.defences.trainer import AdversarialTrainer as AdversarialTrainer_ART

# Own Modules
from classes.DefenseClass import DefenseClass, TrainerDefense
from ml_attacks.evasion.FGM import FGM
from ml_attacks.evasion.PGD import PGD

'''
Class performing adversarial training based on a model architecture and one or multiple attack methods.

Incorporates original adversarial training, ensemble adversarial training (https://arxiv.org/abs/1705.07204), training on all adversarial data and other common setups.
If multiple attacks are specified, they are rotated for each batch. If the specified attacks have as target a different model, then the attack is transferred.
The ratio determines how many of the clean samples in each batch are replaced with their adversarial counterpart.

Warning:
Both successful and unsuccessful adversarial samples are used for training. In the case of unbounded attacks (e.g., DeepFool), this can result in invalid (very noisy) samples being included.

Paper link: https://arxiv.org/abs/1705.07204
Please keep in mind the limitations of defences.
While adversarial training is widely regarded as a promising, principled approach to making classifiers more robust (see https://arxiv.org/abs/1802.00420), very careful evaluations are required to assess its effectiveness case by case (see https://arxiv.org/abs/1902.06705).
'''

class AdversarialTrainer(TrainerDefense):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)
    
    def perform_defense(self):
        # Initializing a vulnerable classsifier
        vulnerable_classifier = self.create_keras_classifier(self.vulnerable_model)
        
        # Initializing a robust classifier
        robust_classifier = self.create_keras_classifier(self.robust_model)
        
        # Training the vulnerable classifier
        train_images_original = self.dataset_struct["train_data"][0]
        train_labels_original = self.dataset_struct["train_data"][1]

        samples_percentage = self.params["samples_percentage"]
        samples = round(samples_percentage * self.dataset_stats["num_train_samples"])
        
        vulnerable_classifier.fit(
            x=train_images_original[:samples],
            y=train_labels_original[:samples],
            nb_epochs=self.params["epochs"]
            )
        
        # Initializing a Evasion attack
        attack = self.params["evasion_attack"]
        attack_params = self.params["evasion_params"]
        if(attack.lower() == "fgm"):
            evasion_attack = FGM(model=None, params=attack_params).perform_attack(vulnerable_classifier)
        elif(attack.lower() == "pgd"):
            evasion_attack = PGD(model=None, params=attack_params).perform_attack(vulnerable_classifier)
        else:
            evasion_attack = None
        
        # Initializing an adversarial trainer to train
        # a robust model
        trainer = AdversarialTrainer_ART(
            classifier=robust_classifier,   # Model to train adversarially (default: CLASSIFIER_LOSS_GRADIENTS_TYPE).
            attacks=evasion_attack,         # Attacks to use for data augmentation in adversarial training
            ratio=self.params["ratio"]      # The proportion of samples in each batch to be replaced with their adversarial counterparts. Setting this value to 1 allows to train only on adversarial samples (default: 0.5).
            )
        
        # Training the robust classifier
        trainer.fit(
            x=train_images_original[:samples],
            y=train_images_original[:samples],
            nb_epochs=self.params["epochs"]
            )
        
        # Generating adversarial samples
        test_images_attack = evasion_attack.generate(x=self.dataset_sturct["test_data"][0])
        
        return test_images_attack, robust_classifier, vulnerable_classifier
        
    def evaluate(self, test_images_attack, robust_classifier, vulnerable_classifier):
        # Evaluating the performance of the vulnerable classier on clean and adversarial images
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        score_clean = vulnerable_classifier._model.evaluate(x=test_images_original, y=test_labels_original)
        score_attack = vulnerable_classifier._model.evaluate(x=test_images_attack, y=test_labels_original)

        # Evaluating the performance of the robust classifier on adversarial images
        score_robust_attack = robust_classifier._model.evaluate(x=test_images_attack, y=test_labels_original)
        
        return score_clean, score_attack, score_robust_attack
        
    def print_stats(self, score_clean, score_attack, score_robust_attack):
        # Comparing test losses
        attack = self.params["evasion_attack"]
        
        print("------ TEST METRICS OF VULNERABLE MODEL ------")
        print(f"Clean test loss: {score_clean[0]:.2f} "
            f"vs {attack} test loss: {score_attack[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test accuracy: {score_clean[1]:.2f} "
            f"vs {attack} test accuracy: {score_attack[1]:.2f}")

        
        # Comparing test losses
        print("------ TEST METRICS OF ROBUST VS VULNERABLE MODEL ON ADVERSARIAL SAMPLES ------")
        print(f"Robust model test loss: {score_robust_attack[0]:.2f} "
            f"vs vulnerable model test loss: {score_attack[0]:.2f}")

        # Comparing test accuracies
        print(f"Robust model test accuracy: {score_robust_attack[1]:.2f} "
            f"vs vulnerable model test accuracy: {score_attack[1]:.2f}")
        
    def plotting_stats(self):
        pass
