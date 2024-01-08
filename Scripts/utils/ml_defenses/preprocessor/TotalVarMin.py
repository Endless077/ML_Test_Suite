# Import Modules
import numpy as np
from art.attacks.evasion import FastGradientMethod
from art.attacks.evasion import ProjectedGradientDescent
from art.defences.preprocessor import TotalVarMin
from art.estimators.classification import KerasClassifier

# Own Modules
from ml_attacks.evasion.FGM import FGM
from ml_attacks.evasion.PGD import PGD
from classes.DefenseClass import DefenseClass, PreprocessorDefense

'''
Implement the total variance minimization defence approach.

Paper link: https://openreview.net/forum?id=SyJ7ClWCb
Please keep in mind the limitations of defences. For more information on the limitations of this defence, see https://arxiv.org/abs/1802.00420.
For details on how to evaluate classifier security in general, see https://arxiv.org/abs/1902.06705
'''

class TotalVarMin(PreprocessorDefense):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)
    
    def perform_defense(self):
        # Initializing the defense
        defense = TotalVarMin(
            prob=0.3,                       # Probability of applying the defense to each sample (default: 0.3)
            norm=2,                         # The norm order to be used for computing the gradient (default: 2)
            lamb=0.5,                       # Regularization parameter (default: 0.5)
            solver='L-BFGS-B',              # The solver to be used (default: 'L-BFGS-B')
            max_iter=10,                    # Maximum number of iterations (default: 10)
            clip_values=None,               # Tuple of min and max values for input clipping or None for no clipping (default: CLIP_VALUES_TYPE)
            apply_fit=False,                # If True, the defense is applied during the fit (default: False)
            apply_predict=True,             # If True, the defense is applied during prediction (default: True)
            verbose=False                   # If True, print information about the adversarial training progress (default: False)
        )
            
        # Initializing a vulnerable classsifier
        vulnerable_classifier = self.create_keras_classifier(self.vulnerable_model)
        
        # Initializing a robust classifier
        # robust_classifier = self.create_keras_classifier(self.robust_model)
        
        # Training the vulnerable classifier
        train_images_original = self.dataset_struct["train_data"][0]
        train_labels_original = self.dataset_struct["train_data"][1]
        
        epochs = self.params["model_params"]["epochs"]
        
        total_var_samples = round(0.1 * self.dataset_stats["num_train_samples"])
        
        vulnerable_classifier.fit(
            x=train_images_original[:samples],
            y=train_labels_original[:samples],
            nb_epochs=epochs
            )
        
        # Initializing a Evasion attack
        attack = self.params["method"].split(':')[1].strip()
        if(attack.lower() == "fgm"):
            evasion_attack = FGM(model=None).perform_attack(vulnerable_classifier)
        elif(attack.lower() == "pgd"):
            evasion_attack = PGD(model=None).perform_attack(vulnerable_classifier)
        else:
            evasion_attack = None

        # Initializing an adversarial trainer to train
        # a robust model
        """
        trainer = AdversarialTrainer(
            classifier=robust_classifier,   # Model to train adversarially (default: CLASSIFIER_LOSS_GRADIENTS_TYPE).
            attacks=evasion_attack,         # Attacks to use for data augmentation in adversarial training
            ratio=0.5                       # The proportion of samples in each batch to be replaced with their adversarial counterparts. Setting this value to 1 allows to train only on adversarial samples (default: 0.5).
            )
        """
        
        # Training the robust classifier
        """
        trainer.fit(
            x=train_images_original[:samples],
            y=train_images_original[:samples],
            nb_epochs=epochs
            )
        """
        
        # Generating adversarial samples
        # Running the defense on adversarial images
        test_images_attack = evasion_attack.generate(x=dataset_sturct["test_data"][0])
        test_images_attack_cleaned = defense(test_images_attack[:total_var_samples])[0]
        
        return test_images_attack, test_images_attack_cleaned, vulnerable_classifier
        
    def evaluate(self, test_images_attack, robust_classifier, vulnerable_classifier):
        # Evaluating the performance of the vulnerable classifier on adversarial and cleaned images
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        total_var_samples = round(0.1 * self.dataset_stats["num_train_samples"])
        
        score_attack = vulnerable_classifier._model.evaluate(x=test_images_attack[:total_var_samples], y=test_labels_original[:total_var_samples])
        score_attack_cleaned = vulnerable_classifier._model.evaluate(x=test_images_attack_cleaned, y=test_labels_original[:total_var_samples])
        
        return score_attack, score_attack_cleaned
    
    def print_stats(self, score_attack, score_attack_cleaned):
        # Comparing test losses
        print("------ TEST METRICS ON ADVERSARIAL AND CLEANED IMAGES ------")
        print(f"Test loss on adversarial images: {score_attack[0]:.2f} "
            f"vs test loss on cleaned images: {score_attack_cleaned[0]:.2f}")

        # Comparing test accuracies
        print(f"Test accuracy on adversarial images: {score_attack[1]:.2f} "
            f"vs test accuracy on cleaned images: {score_fgm_cleaned[1]:.2f}")
        
    def plotting_stats(self):
        pass
