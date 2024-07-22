# ProjectedGradientDescent ART Class
from art.attacks.evasion import ProjectedGradientDescent

# Own Modules
from classes.AttackClass import EvasionAttack

# Utils
from utils.model import *

'''
The Projected Gradient Descent attack is an iterative method in which, after each iteration, the perturbation is projected on an lp-ball of specified radius (in addition to clipping the values of the adversarial sample so that it lies in the permitted data range).
This is the attack proposed by Madry et al. for adversarial training.

Paper link: https://arxiv.org/abs/1706.06083
'''

TAG = "PGD"

class PGD(EvasionAttack):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)

    def perform_attack(self):
        # Create a Keras Classifier
        print(f"[{TAG}] Create a Keras Classifier")
        evasion_classifier = self.create_keras_classifier(self.model)
        
        # Defining an attack using the fast gradient method
        print(f"[{TAG}] Defining an attack using the fast gradient method")
        attack_pgdm = ProjectedGradientDescent(
            estimator=evasion_classifier,                   # The classifier or object detector used for crafting adversarial examples (default: CLASSIFIER_LOSS_GRADIENTS_TYPE) 
            norm=self.params["norm"],               # The norm used for measuring the size of the perturbation (default: infinity norm)
            eps=self.params["eps"],                 # The magnitude of the perturbation (default: 0.3)
            eps_step=self.params["eps_step"],       # The step size of the perturbation (default: 0.1)
            decay=None,                             # The decay factor for the learning rate (default: None)
            max_iter=100,                           # The maximum number of iterations (default: 100)
            targeted=False,                         # If True, performs a targeted attack; if False, performs an untargeted attack (default: False)
            num_random_init=0,                      # The number of random initializations for the attack (default: 0)
            batch_size=self.params["batch_size"],   # The batch size for the attack (default: 32)
            random_eps=False,                       # If True, uses random perturbation instead of fixed perturbation (default: False)
            summary_writer=False,                   # If True, enables writing of summaries for TensorBoard (default: False)
            verbose=True                            # If True, prints progress information during the attack (default: True)
        )
        
        return attack_pgdm
    
    def evaluate(self, attack_pgdm):
        # Generating adversarial images from test images
        print(f"[{TAG}] Generating adversarial images from test images")
        x_test_adv = attack_pgdm.generate(x=self.dataset_struct["test_data"][0])
        
        # Evaluating the model on clean images
        print(f"[{TAG}] Evaluating the model on clean images")
        score_clean = self.model.evaluate(
            x=self.dataset_struct["test_data"][0],
            y=self.dataset_struct["test_data"][1]
            )

        # Evaluating the model on adversarial images
        print(f"[{TAG}] Evaluating the model on adversarial images")
        score_adv = self.model.evaluate(
            x=x_test_adv,
            y=self.dataset_struct["test_data"][1]
            )
        
        return score_clean, score_adv
    
    def plotting_stats(self):
        raise NotImplementedError
    
    def result(self, score_clean, score_adv):
        # Comparing test losses
        print(f"Clean test set loss: {score_clean[0]:.2f} "
            f"vs adversarial set test loss: {score_adv[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test set accuracy: {score_clean[1]:.2f} "
            f"vs adversarial test set accuracy: {score_adv[1]:.2f}")
        
        # Build summary model and result
        print(f"[{TAG}] Build summary model and result")
        summary_dict = summary_model(self.model)
        
        result_dict = {
            "clean_scores": {
                "loss": f"{score_clean[0]:.2f}",
                "accuracy": f"{score_clean[1]:.2f}"
            },
            "adv_scores": {
                "loss": f"{score_adv[0]:.2f}",
                "accuracy": f"{score_adv[1]:.2f}"
            },
            "summary": summary_dict
        }
        
        # Save Summary File
        print(f"[{TAG}] Save Summary File")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
