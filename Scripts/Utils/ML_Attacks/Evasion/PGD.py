#Import Modules
from art.attacks.evasion import ProjectedGradientDescent
from art.estimators.classification import KerasClassifier
from art.estimators.classification import CLASSIFIER_LOSS_GRADIENTS_TYPE

'''
The Projected Gradient Descent attack is an iterative method in which, after each iteration, the perturbation is projected on an lp-ball of specified radius (in addition to clipping the values of the adversarial sample so that it lies in the permitted data range).
This is the attack proposed by Madry et al. for adversarial training.

Paper link: https://arxiv.org/abs/1706.06083
'''

class PGD:
    def __init__(self, dataset_struct, dataset_stats, model, params):
        self.dataset_struct = dataset_struct
        self.dataset_stats = dataset_stats
        self.model_original = model
        self.params = params
        
    def create_keras_classifier():
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        classifier_original = KerasClassifier(
            model=self.model_original,      # The Keras model (if none)
            use_logits=False,               # Use logit outputs instead of probabilities
            channel_index=-1,               # Index of the channel axis in the input data
            preprocessing_defences=None,    # Defenses for pre-processing the data
            postprocessing_defences=None,   # Defenses for post-processing the results
            input_layer=0,                  # Input layer of the model
            output_layer=-1,                # Output layer of the model
            channels_first=False,           # Whether channels are the first dimension in the input data
            clip_values=(0, 1)              # Range of valid input values
        )
        
        return classifier_original
    
    def perform_pgd_attack(classifier):
        # Defining an attack using the fast gradient method
        attack_pgdm = ProjectedGradientDescent(
            estimator=classifier,       # The classifier or object detector used for crafting adversarial examples (default: CLASSIFIER_LOSS_GRADIENTS_TYPE) 
            norm=float('inf'),          # The norm used for measuring the size of the perturbation (default is infinity norm)
            eps=0.3,                    # The magnitude of the perturbation (default is 0.3)
            eps_step=0.1,               # The step size of the perturbation (default is 0.1)
            decay=None,                 # The decay factor for the learning rate (default is None)
            max_iter=100,               # The maximum number of iterations (default is 100)
            targeted=False,             # If True, performs a targeted attack; if False, performs an untargeted attack (default is False)
            num_random_init=0,          # The number of random initializations for the attack (default is 0)
            batch_size=32,              # The batch size for the attack (default is 32)
            random_eps=False,           # If True, uses random perturbation instead of fixed perturbation (default is False)
            summary_writer=False,       # If True, enables writing of summaries for TensorBoard (default is False)
            verbose=True                # If True, prints progress information during the attack (default is True)
        )
        
        # Generating adversarial images from test images
        x_test_adv = attack_pgdm.generate(x=dataset_struct["test_data"][0])
        
        y_test = dataset_struct["test_data"][1]
        return x_test_adv
    
    def evaluate_fgm_models(x_test_adv):
        # Evaluating the model on clean images
        score_clean = model.evaluate(
            x=dataset_struct["test_data"][0],
            y=dataset_struct["test_data"][1]
            )

        # Evaluating the model on adversarial images
        score_adv = model.evaluate(
            x=x_test_adv,
            y=dataset_struct["test_data"][1]
            )
        
        return score_clean, score_adv

    def print_stats(score_clean, score_adv):
        # Comparing test losses
        print(f"Clean test set loss: {score_clean[0]:.2f} "
            f"vs adversarial set test loss: {score_adv[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test set accuracy: {score_clean[1]:.2f} "
            f"vs adversarial test set accuracy: {score_adv[1]:.2f}")
    
    def plotting_stats(score_clean, score_adv):
        pass
    