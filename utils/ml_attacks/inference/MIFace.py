# Import Modules
import numpy as np
from art.attacks.inference.model_inversion import MIFace as MIFace_ART

# Own Modules
from classes.AttackClass import AttackClass, InferenceAttack

'''
Implementation of the MIFace algorithm from Fredrikson et al. (2015).
While in that paper the attack is demonstrated specifically against face recognition models, it is applicable more broadly to classifiers with continuous features which expose class gradients.

Paper link: https://dl.acm.org/doi/10.1145/2810103.2813677
'''

class MIFace(InferenceAttack):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
    
    def perform_attack(self, classifier):
        # Defining a model inversion attack
        attack = MIFace_ART(
            classifier=classifier,                          # The classifier used for crafting adversarial examples (default: CLASSIFIER_LOSS_GRADIENTS_TYPE)
            max_iter=self.params["max_iter"],               # Maximum number of gradient descent iterations for the model inversion (default: 10000)
            window_length=self.params["window_length"],     # Length of window for checking whether descent should be aborted (default: 100)
            threshold=self.params["threshold"],             # Threshold for descent stopping criterion (default: 0.99)
            learning_rate=self.params["learning_rate"],     # Learning rate (default: 0.1)
            batch_size=self.params["batch_size"],           # Size of internal batches (default: 256)
            verbose=True                                    # Print debug information during execution (default: True)
        )
    
        # Get some dataset stats
        num_classes = self.dataset_stats["num_classes"]
        
        image_shape = self.dataset_stats["image_shape"]
        shape_x = image_shape[0]
        shape_y = image_shape[1]
        channels = image_shape[2]
        
        # Defining the target labels for model inversion
        y = np.arange(start=0, stop=num_classes)
        
        # Inspecting the target labels
        print(y)

        # Defining an initialization array for model inversion
        x_init_average = np.zeros(shape=(num_classes, shape_x, shape_y, channels)) + np.mean(a=self.dataset_struct["test_data"][0], axis=0)
        
        # Checking class gradients
        class_gradient = classifier.class_gradient(
            x=x_init_average,
            label=y
            )

        # Reshaping class gradients
        class_gradient = np.reshape(
            a=class_gradient,
            newshape=(num_classes, shape_x*shape_y*channels)
            )

        # Obtaining the largest gradient value for each class
        class_gradient_max = np.max(class_gradient, axis=1)

        # Inspecting class gradients
        print(class_gradient_max)

        # Running model inversion
        # %%time
        x_infer_from_average = attack.infer(
            x=x_init_average,
            y=y
            )
        
        return x_infer_from_average
    
    def evaluate(self):
        pass

    def print_stats(self, score_clean, score_adv):
        pass
    
    def plotting_stats(self, score_clean, score_adv):
        pass