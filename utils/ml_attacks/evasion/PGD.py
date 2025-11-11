# ProjectedGradientDescent ART Class
from art.attacks.evasion import ProjectedGradientDescent

# Own Modules
from classes.AttackClass import EvasionAttack

# Utils
from utils.model import *

TAG = "PGD"

class PGD(EvasionAttack):
    """
    Projected Gradient Descent (PGD) attack class.

    This class implements the Projected Gradient Descent attack for generating adversarial examples.
    
    PGD is an iterative method where the perturbation is projected onto an lp-ball of a specified
    radius after each iteration, in addition to clipping the values of the adversarial sample so that it lies
    within the permitted data range. It is commonly used for adversarial training as described by Madry et al. (2017).
        
    Paper: https://arxiv.org/abs/1706.06083
    """
    def __init__(self, model, dataset_struct, dataset_stats, params):
        """
        Initialize the PGD attack instance.

        Parameters:
        - model (tf.keras.Model): The Keras model to attack.
        - dataset_struct (Dict[str, tf.Tensor]): Dictionary containing training and test data.
        - dataset_stats (Dict[str, Any]): Dictionary containing dataset statistics.
        - params (Dict[str, Any]): Dictionary containing parameters for the attack.
        """
        super().__init__(model, dataset_struct, dataset_stats, params)

    def perform_attack(self, classifier):
        """
        Define the Projected Gradient Descent attack.

        Parameters:
        - classifier (ProjectedGradientDescent): The classifier used to craft adversarial examples.

        Returns:
        - attack_pgd (ProjectedGradientDescent): An instance of the Projected Gradient Descent attack.
        """
        # Defining an attack using the fast gradient method
        print(f"[{TAG}] Defining an attack using the fast gradient method")
        attack_pgd = ProjectedGradientDescent(
            estimator=classifier,                   # The classifier or object detector used for crafting adversarial examples (default: CLASSIFIER_LOSS_GRADIENTS_TYPE) 
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
        
        return attack_pgd
    
    def evaluate(self, attack_pgd):
        """
        Evaluate the model on clean and adversarial examples.

        Parameters:
        - attack_pgd (ProjectedGradientDescent): The Projected Gradient Descent attack instance.

        Returns:
        - Tuple[Tuple[float, float], Tuple[float, float]]: Scores on clean images and adversarial images.
        """ 
        # Generating adversarial images from test images
        print(f"[{TAG}] Generating adversarial images from test images")
        x_test_adv = attack_pgd.generate(x=self.dataset_struct["test_data"][0])
        
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
        
        # Build summary model and result
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
