# AdversarialTrainer ART Class
from art.defences.trainer import AdversarialTrainer as AdversarialTrainer_ART

# Own Modules
from ml_attacks.evasion.FGM import FGM
from ml_attacks.evasion.PGD import PGD
from classes.DefenseClass import TrainerDefense

# Utils
from utils.model import *

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

TAG = "AdversarialTrainer"

class AdversarialTrainer(TrainerDefense):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)
    
    def perform_defense(self):
        # Initializing a vulnerable classsifier
        print(f"[{TAG}] Initializing a vulnerable classsifier")
        vulnerable_classifier = self.create_keras_classifier(self.vulnerable_model)
        
        # Initializing a robust classifier
        print(f"[{TAG}] Initializing a robust classifier")
        robust_classifier = self.create_keras_classifier(self.robust_model)
        
        # Training the vulnerable classifier
        print(f"[{TAG}] Training the vulnerable classifier")
        train_images_original = self.dataset_struct["train_data"][0]
        train_labels_original = self.dataset_struct["train_data"][1]

        samples_percentage = self.params["samples_percentage"]
        samples = round(samples_percentage * self.dataset_stats["num_train_samples"])
        
        # Fit the vulnerable classifier
        print(f"[{TAG}] Fit the vulnerable classifier")
        vulnerable_classifier.fit(
            x=train_images_original[:samples],
            y=train_labels_original[:samples],
            nb_epochs=self.params["epochs"],
            batch_size=self.params["batch_size"],
            verbose=True
            )
        
        # Initializing a Evasion attack
        print(f"[{TAG}] Initializing a Evasion attack")
        attack = self.params["evasion_attack"]
        attack_params = {
            "epochs": self.params["epochs"],
            "batch_size": self.params["batch_size"],
            "eps": self.params["eps"],
            "eps_step": self.params["eps_step"],
            "norm": self.params["norm"]
        }
        if(attack.lower() == "fgm"):
            evasion_attack = FGM(model=None, dataset_struct=None, dataset_stats=None, params=attack_params).perform_attack(vulnerable_classifier)
        elif(attack.lower() == "pgd"):
            evasion_attack = PGD(model=None, dataset_struct=None, dataset_stats=None, params=attack_params).perform_attack(vulnerable_classifier)
        else:
            evasion_attack = None
        
        # Initializing an adversarial trainer to train a robust model
        print(f"[{TAG}] Initializing an adversarial trainer to train a robust model")
        trainer = AdversarialTrainer_ART(
            classifier=robust_classifier,   # Model to train adversarially (default: CLASSIFIER_LOSS_GRADIENTS_TYPE).
            attacks=evasion_attack,         # Attacks to use for data augmentation in adversarial training
            ratio=self.params["ratio"]      # The proportion of samples in each batch to be replaced with their adversarial counterparts. Setting this value to 1 allows to train only on adversarial samples (default: 0.5).
            )
        
        # Training the robust classifier
        print(f"[{TAG}] Training the robust classifier")
        trainer.fit(
            x=train_images_original[:samples],
            y=train_labels_original[:samples],
            nb_epochs=self.params["epochs"],
            batch_size=self.params["batch_size"],
            verbose=True
            )
        
        # Generating adversarial samples
        print(f"[{TAG}] Generating adversarial samples")
        test_images_attack = evasion_attack.generate(x=self.dataset_struct["test_data"][0])
        
        return test_images_attack, robust_classifier, vulnerable_classifier
        
    def evaluate(self, test_images_attack, robust_classifier, vulnerable_classifier):
        # Evaluating the performance of the vulnerable classier on clean and adversarial images
        print(f"[{TAG}] Evaluating the performance of the vulnerable classier on clean and adversarial images")
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        score_clean = vulnerable_classifier._model.evaluate(x=test_images_original, y=test_labels_original)
        score_attack = vulnerable_classifier._model.evaluate(x=test_images_attack, y=test_labels_original)

        # Evaluating the performance of the robust classifier on adversarial images
        print(f"[{TAG}] Evaluating the performance of the robust classifier on adversarial images")
        score_robust_attack = robust_classifier._model.evaluate(x=test_images_attack, y=test_labels_original)
        
        return score_clean, score_attack, score_robust_attack
        
    def plotting_stats(self):
        raise NotImplementedError
    
    def result(self, score_clean, score_attack, score_robust_attack):
        # Checking Test Metrics of Vulnerable Model
        print(f"[{TAG}] Checking Test Metrics of Vulnerable Model")
        
        # Comparing tes losses
        print(f"Clean test loss: {score_clean[0]:.2f} "
            f"vs evasion attack test loss: {score_attack[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test accuracy: {score_clean[1]:.2f} "
            f"vs evasion attack test accuracy: {score_attack[1]:.2f}")

        # Checking Test Metrics of Robust vs Vulnerable on Adv Samples
        print(f"[{TAG}] Checking Test Metrics of Robust vs Vulnerable on Adv Samples")
        
        # Comparing test losses
        print(f"Robust model test loss: {score_robust_attack[0]:.2f} "
            f"vs vulnerable model test loss: {score_attack[0]:.2f}")

        # Comparing test accuracies
        print(f"Robust model test accuracy: {score_robust_attack[1]:.2f} "
            f"vs vulnerable model test accuracy: {score_attack[1]:.2f}")
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        vulnerable_model_summary_dict = summary_model(self.vulnerable_model)
        robust_model_summary_dict = summary_model(self.robust_model)
        
        result_dict = {
            "vulnerable_model_metrics": {
                "loss": {
                    "clean_test": f"{score_clean[0]:.2f}",
                    f"evasion_attack_test": f"{score_attack[0]:.2f}"
                },
                "accuracy": {
                    "clean_test": f"{score_clean[1]:.2f}",
                    f"evasion_attack_test": f"{score_attack[1]:.2f}"
                }
            },
            "comparison_model_metrics": {
                "loss": {
                    "robust": f"{score_robust_attack[0]:.2f}",
                    "vulnerable": f"{score_attack[0]:.2f}"
                },
                "accuracy": {
                    "robust": f"{score_robust_attack[1]:.2f}",
                    "vulnerable": f"{score_attack[1]:.2f}"
                }
            },
            "robust_model_summary": robust_model_summary_dict,
            "vulnerable_model_summary": vulnerable_model_summary_dict
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
