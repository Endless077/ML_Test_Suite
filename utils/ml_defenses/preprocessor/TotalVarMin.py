# TotalVarMin ART Class
from art.defences.preprocessor import TotalVarMin as TotalVarMin_ART

# Own Modules
from ml_attacks.evasion.FGM import FGM
from ml_attacks.evasion.PGD import PGD
from classes.DefenseClass import DefenseClass, PreprocessorDefense

# Utils
from utils.model import *

'''
Implement the total variance minimization defence approach.

Paper link: https://openreview.net/forum?id=SyJ7ClWCb
Please keep in mind the limitations of defences. For more information on the limitations of this defence, see https://arxiv.org/abs/1802.00420.
For details on how to evaluate classifier security in general, see https://arxiv.org/abs/1902.06705
'''

TAG = "TotalVarMin"

class TotalVarMin(PreprocessorDefense):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def perform_defense(self):
        # Initializing the defense
        print(f"[{TAG}] Initializing the defense")
        defense = TotalVarMin_ART(
            prob=self.params["prob"],           # Probability of applying the defense to each sample (default: 0.3)
            norm=self.params["norm_value"],     # The norm order to be used for computing the gradient (default: 2)
            lamb=self.params["lamb_value"],     # Regularization parameter (default: 0.5)
            solver=self.params["solver"],       # The solver to be used (default: 'L-BFGS-B')
            max_iter=self.params["max_iter"],   # Maximum number of iterations (default: 10)
            clip_values=None,                   # Tuple of min and max values for input clipping or None for no clipping (default: CLIP_VALUES_TYPE)
            apply_fit=False,                    # If True, the defense is applied during the fit (default: False)
            apply_predict=True,                 # If True, the defense is applied during prediction (default: True)
            verbose=True                        # If True, print information about the adversarial training progress (default: False)
        )
        
        # Initializing a vulnerable classifier
        print(f"[{TAG}] Initializing a vulnerable classifier")
        vulnerable_classifier = self.create_keras_classifier(self.model)
        
        # Initializing a robust classifier
        #print(f"[{TAG}] Initializing a robust classifier")
        # robust_classifier = self.create_keras_classifier(self.model)
        
        # Training the vulnerable classifier
        print(f"[{TAG}] Training the vulnerable classifier")
        train_images_original = self.dataset_struct["train_data"][0]
        train_labels_original = self.dataset_struct["train_data"][1]
        
        samples_percentage = self.params["samples_percentage"]
        total_var_samples = round(samples_percentage * self.dataset_stats["num_test_samples"])
        
        vulnerable_classifier.fit(
            x=train_images_original,
            y=train_labels_original,
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
        #print(f"[{TAG}] Initializing an adversarial trainer to train a robust model")
        """
        trainer = AdversarialTrainer(
            classifier=robust_classifier,   # Model to train adversarially (default: CLASSIFIER_LOSS_GRADIENTS_TYPE).
            attacks=evasion_attack,         # Attacks to use for data augmentation in adversarial training
            ratio=0.5                       # The proportion of samples in each batch to be replaced with their adversarial counterparts. Setting this value to 1 allows to train only on adversarial samples (default: 0.5).
            )
        """
        
        # Training the robust classifier
        #print(f"[{TAG}] Training the robust classifier")
        """
        trainer.fit(
            x=train_images_original[:samples],
            y=train_images_original[:samples],
            nb_epochs=epochs
            )
        """
        
        # Generating adversarial samples
        print(f"[{TAG}] Generating adversarial samples")
        test_images_attack = evasion_attack.generate(x=self.dataset_struct["test_data"][0])
        
        # Running the defense on adversarial images
        print(f"[{TAG}] Running the defense on adversarial images")
        test_images_attack_cleaned = defense(test_images_attack[:total_var_samples])[0]
        
        return test_images_attack, test_images_attack_cleaned, vulnerable_classifier
        
    def evaluate(self, test_images_attack, test_images_attack_cleaned, vulnerable_classifier):
        # Evaluating the performance of the vulnerable classifier on adversarial and cleaned images
        print(f"[{TAG}] Evaluating the performance of the vulnerable classifier on adversarial and cleaned images")
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        samples_percentage = self.params["samples_percentage"]
        total_var_samples = round(samples_percentage * self.dataset_stats["num_test_samples"])
        
        score_attack = vulnerable_classifier._model.evaluate(x=test_images_attack[:total_var_samples], y=test_labels_original[:total_var_samples])
        score_attack_cleaned = vulnerable_classifier._model.evaluate(x=test_images_attack_cleaned, y=test_labels_original[:total_var_samples])
        
        return score_attack, score_attack_cleaned
        
    def plotting_stats(self):
        raise NotImplementedError
    
    def result(self, score_attack, score_attack_cleaned):
        # Comparing test losses
        print(f"[{TAG}] Comparing test losses")
        print(f"Test loss on adversarial images: {score_attack[0]:.2f} "
            f"vs test loss on cleaned images: {score_attack_cleaned[0]:.2f}")

        # Comparing test accuracies
        print(f"[{TAG}] Comparing test accuracies")
        print(f"Test accuracy on adversarial images: {score_attack[1]:.2f} "
            f"vs test accuracy on cleaned images: {score_attack_cleaned[1]:.2f}")
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "loss": {
                "cleaned_images": f"{score_attack_cleaned[0]:.2f}",
                "adv_images": f"{score_attack[0]:.2f}",
            },
            "accuracy": {
                "cleaned_images": f"{score_attack_cleaned[1]:.2f}",
                "adv_images": f"{score_attack[1]:.2f}",
            },
            "params": self.params,
            "summary": summary
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
