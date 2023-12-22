#Import Modules
from art.attacks.inference.model_inversion import MIFace
from art.estimators.classification import KerasClassifier
from art.estimators.classification import CLASSIFIER_LOSS_GRADIENTS_TYPE

#Own Modules
from Class import AttackClass

'''
Implementation of the MIFace algorithm from Fredrikson et al. (2015).
While in that paper the attack is demonstrated specifically against face recognition models, it is applicable more broadly to classifiers with continuous features which expose class gradients.

Paper link: https://dl.acm.org/doi/10.1145/2810103.2813677
'''

class MIFace(AttackClass):
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
        # Defining a model inversion attack
        attack = MIFace(
            classifier=classifier,  # The classifier used for crafting adversarial examples (default: CLASSIFIER_LOSS_GRADIENTS_TYPE)
            max_iter=2500,          # Maximum number of gradient descent iterations for the model inversion (default: 10000)
            window_length=100,      # Length of window for checking whether descent should be aborted (default: 100)
            threshold=0.99,         # Threshold for descent stopping criterion (default: 0.99)
            learning_rate=0.1,      # Learning rate (default: 0.1)
            batch_size=256,         # Size of internal batches (default: 256)
            verbose=True            # Print debug information during execution (default: True)
        )
    
        # Get some dataset stats
        num_classes = dataset_stats["num_classes"]
        
        imge_shape = dataset_stats["image_shape"]
        shape_x = imge_shape[0]
        shape_y = imge_shape[1]
        channels = imge_shape[2]
        
        # Defining the target labels for model inversion
        y = np.arange(start=0, stop=num_classes)
        
        # Inspecting the target labels
        print(y)

        # Defining an initialization array for model inversion
        x_init_average = np.zeros(shape=(num_classes, shape_x, shape_y, channels)) + np.mean(a=dataset_struct["test_data"][0], axis=0)
        
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
    
    def evaluate(self, x_test_adv):
        pass

    def print_stats(self, scores_clean, scores_adv):
        pass
    
    def plotting_stats(self, scores_clean, scores_adv):
        pass