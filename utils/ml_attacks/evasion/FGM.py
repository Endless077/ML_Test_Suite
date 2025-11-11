# FastGradientMethod ART Class
from art.attacks.evasion import FastGradientMethod

# Own Modules
from classes.AttackClass import EvasionAttack

# Utils
from utils.model import *

TAG = "FGM"

class FGM(EvasionAttack):
    """
    Fast Gradient Method (FGM) attack class.

    This class implements the Fast Gradient Method for generating adversarial examples.
    It extends the attack to various norms beyond the infinity norm, as originally described by Goodfellow et al. (2015).
    
    Paper: https://arxiv.org/abs/1412.6572
    """
    def __init__(self, model, dataset_struct, dataset_stats, params):
        """
        Initialize the FGM attack instance.

        Parameters:
        - model (tf.keras.Model): The Keras model to attack.
        - dataset_struct (Dict[str, tf.Tensor]): Dictionary containing training and test data.
        - dataset_stats (Dict[str, Any]): Dictionary containing dataset statistics.
        - params (Dict[str, Any]): Dictionary containing parameters for the attack.
        """
        super().__init__(model, dataset_struct, dataset_stats, params)

    def perform_attack(self, classifier):
        """
        Define the Fast Gradient Method attack.

        Parameters:
        - classifier (FastGradientMethod): The classifier used to craft adversarial examples.

        Returns:
        - attack_fgm (FastGradientMethod): An instance of the Fast Gradient Method attack.
        """
        # Defining an attack using the fast gradient method
        print(f"[{TAG}] Defining an attack using the fast gradient method")
        attack_fgm = FastGradientMethod(
            estimator=classifier,                   # The classifier used for crafting adversarial examples (default: CLASSIFIER_LOSS_GRADIENTS_TYPE)
            norm=self.params["norm"],               # The norm used for measuring the size of the perturbation (default: infinity norm)
            eps=self.params["eps"],                 # The magnitude of the perturbation (default: 0.3)
            eps_step=self.params["eps_step"],       # The step size of the perturbation (default: 0.1)
            targeted=False,                         # If True, performs a targeted attack; if False, performs an untargeted attack (default: False)
            num_random_init=0,                      # The number of random initializations for the attack (default: 0)
            batch_size=self.params["batch_size"],   # The batch size for the attack (default: 32)
            minimal=False,                          # If True, performs minimal perturbation by finding the smallest possible perturbation that changes the prediction (default: False)
            summary_writer=False                    # If True, enables writing of summaries for TensorBoard (default: False)
        )
        
        return attack_fgm
    
    def evaluate(self, attack_fgm):
        """
        Evaluate the model on clean and adversarial examples.

        Parameters:
        - attack_fgm (FastGradientMethod): The Fast Gradient Method attack instance.

        Returns:
        - Tuple[Tuple[float, float], Tuple[float, float]]: Scores on clean images and adversarial images.
        """ 
        # Generating adversarial images from test images
        print(f"[{TAG}] Generating adversarial images from test images")
        x_test_adv = attack_fgm.generate(x=self.dataset_struct["test_data"][0])
        
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
        """
        This method is not implemented. It should handle plotting statistics if required.

        Raises:
        - NotImplementedError: This method has not been implemented yet.
        """
        raise NotImplementedError
    
    def result(self, score_clean, score_adv):
        """
        Print and save the results of the attack evaluation.

        Parameters:
        - score_clean (Tuple[float, float]): Loss and accuracy scores on clean images.
        - score_adv (Tuple[float, float]): Loss and accuracy scores on adversarial images.

        Returns:
        - result_dict (Dict[str, Any]): Dictionary containing the results of the attack.
        """
        # Comparing test losses
        print(f"Clean test set loss: {score_clean[0]:.2f} "
            f"vs adversarial set test loss: {score_adv[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test set accuracy: {score_clean[1]:.2f} "
            f"vs adversarial test set accuracy: {score_adv[1]:.2f}")
        
        # Build summary model and results
        print(f"[{TAG}] Build summary model and results")
        summary = summary_model(self.model)
        
        result_dict = {
            "clean_scores": {
                "loss": f"{score_clean[0]:.2f}",
                "accuracy": f"{score_clean[1]:.2f}"
            },
            "adv_scores": {
                "loss": f"{score_adv[0]:.2f}",
                "accuracy": f"{score_adv[1]:.2f}"
            },
            "params": self.params,
            "summary": summary
        }
        
        # Save summary files
        print(f"[{TAG}] Save summary files")
        self.save_summary(tag=TAG, result=result_dict)
        
        return result_dict
