#Import Modules
from art.attacks.poisoning import PoisoningAttackBackdoor, PoisoningAttackCleanLabelBackdoor
from art.attacks.poisoning.perturbations import add_pattern_bd
from art.estimators.classification import KerasClassifier
from art.utils import to_categorical

#Own Modules
from Class import AttackClass

'''
Implementation of backdoor attacks introduced in Gu et al., 2017.
Applies a number of backdoor perturbation functions and switches label to target label.

Paper link: https://arxiv.org/abs/1708.06733
'''

'''
Implementation of Clean-Label Backdoor Attack introduced in Turner et al., 2018.
Applies a number of backdoor perturbation functions and does not change labels.

Paper link: https://people.csail.mit.edu/madry/lab/cleanlabel.pdf
'''

class Backdoor(AttackClass):
    def __init__(self, dataset_struct, dataset_stats, model, params):
        super().__init__(dataset_struct, dataset_stats, model, params)
    
    def create_keras_classifier(self, poisioned_model):
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        poisioned_classifier = KerasClassifier(
            model=poisioned_model,          # The Keras model
            use_logits=False,               # Use logit outputs instead of probabilities (default: False)
            channel_index=-1,               # Index of the channel axis in the input data (default: -1)
            preprocessing_defences=None,    # Defenses for pre-processing the data (default: None)
            postprocessing_defences=None,   # Defenses for post-processing the results (default: None)
            input_layer=0,                  # Input layer of the model (default: 0)
            output_layer=-1,                # Output layer of the model (default: -1)
            channels_first=False,           # Whether channels are the first dimension in the input data (default: False)
            clip_values=(0, 1)              # Range of valid input values (default: (0,1))
        )
        
        return poisioned_classifier
        
    def perform_attack(self):
        pass
    
    def evaluate(self, model_poisoned, test_poisioned):
        # Evaluating the model on clean images
        score_clean = model_poisoned.evaluate(
            x=dataset_struct["test_data"][0],
            y=dataset_struct["test_data"][1]
            )

        # Evaluating the model on adversarial images
        score_adv = model_poisoned.evaluate(
            x=test_poisioned[0],
            y=test_poisioned[1]
            )
        
        return scores_clean, scores_adv

    def print_stats(self, scores_clean, scores_adv):
        # Comparing test losses
        print(f"Clean test loss: {scores_clean[0]:.2f} "
            f"vs poisoned test loss: {scores_poisoned[0]:.2f}")

        # Comparing test accuracies
        print(f"Clean test accuracy: {scores_clean[1]:.2f} "
            f"vs poisoned test accuracy: {scores_poisoned[1]:.2f}")
    
    def plotting_stats(self, scores_clean, scores_adv):
        pass

def setup_posion(num_poision):
    pass
    
def setup_backdoor():
    pass
