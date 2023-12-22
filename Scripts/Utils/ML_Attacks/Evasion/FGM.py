#Import Modules
from art.attacks.evasion import FastGradientMethod
from art.estimators.classification import KerasClassifier
from art.estimators.classification import CLASSIFIER_LOSS_GRADIENTS_TYPE

#Own Modules
from Class import AttackClass

'''
This attack was originally implemented by Goodfellow et al. (2015) with the infinity norm (and is known as the “Fast Gradient Sign Method”).
This implementation extends the attack to other norms, and is therefore called the Fast Gradient Method.

Paper link: https://arxiv.org/abs/1412.6572
'''

class FGM(AttackClass):
    def __init__(self, dataset_struct, dataset_stats, model, params):
        super().__init__(dataset_struct, dataset_stats, model, params)
        
    def create_keras_classifier(self):
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        classifier = KerasClassifier(
            model=self.model_original,      # The Keras model
            use_logits=False,               # Use logit outputs instead of probabilities (default: False)
            channel_index=-1,               # Index of the channel axis in the input data (default: -1)
            preprocessing_defences=None,    # Defenses for pre-processing the data (default: None)
            postprocessing_defences=None,   # Defenses for post-processing the results (default: None)
            input_layer=0,                  # Input layer of the model (default: 0)
            output_layer=-1,                # Output layer of the model (default: -1)
            channels_first=False,           # Whether channels are the first dimension in the input data (default: False)
            clip_values=(0, 1)              # Range of valid input values (default: (0,1))
        )
        
        return classifier
    
    def perform_attack(self, classifier):
        # Defining an attack using the fast gradient method
        attack_fgsm = FastGradientMethod(
            estimator=classifier,       # The classifier used for crafting adversarial examples (default: CLASSIFIER_LOSS_GRADIENTS_TYPE)
            norm=float('inf'),          # The norm used for measuring the size of the perturbation (default: infinity norm)
            eps=0.3,                    # The magnitude of the perturbation (default: 0.3)
            eps_step=0.1,               # The step size of the perturbation (default: 0.1)
            targeted=False,             # If True, performs a targeted attack; if False, performs an untargeted attack (default: False)
            num_random_init=0,          # The number of random initializations for the attack (default: 0)
            batch_size=32,              # The batch size for the attack (default: 32)
            minimal=False,              # If True, performs minimal perturbation by finding the smallest possible perturbation that changes the prediction (default: False)
            summary_writer=False        # If True, enables writing of summaries for TensorBoard (default: False)
        )
        
        # Generating adversarial images from test images
        x_test_adv = attack_fgsm.generate(x=dataset_struct["test_data"][0])
        
        y_test = dataset_struct["test_data"][1]
        return x_test_adv
    
    def evaluate(self, x_test_adv):
        # Evaluating the model on clean images
        score_clean = self.model.evaluate(
            x=dataset_struct["test_data"][0],
            y=dataset_struct["test_data"][1]
            )

        # Evaluating the model on adversarial images
        score_adv = self.model.evaluate(
            x=x_test_adv,
            y=dataset_struct["test_data"][1]
            )
        
        return scores_clean, scores_adv

    def print_stats(self, scores_clean, scores_adv):
        # Comparing test losses
        print(f"Clean test set loss: {scores_clean[0]:.2f} "
            f"vs adversarial set test loss: {scores_adv[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test set accuracy: {scores_clean[1]:.2f} "
            f"vs adversarial test set accuracy: {scores_adv[1]:.2f}")
    
    def plotting_stats(self, scores_clean, scores_adv):
        pass
    