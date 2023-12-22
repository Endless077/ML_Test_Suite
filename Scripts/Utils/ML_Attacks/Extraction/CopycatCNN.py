#Import Modules
from art.attacks.extraction import CopycatCNN
from art.estimators.classification import KerasClassifier

#Own Modules
from Utils import model as mdl
from Class import AttackClass

'''
Implementation of the Copycat CNN attack from Rodrigues Correia-Silva et al. (2018).

Paper link: https://arxiv.org/abs/1806.05476
'''

class CopycatCNN(AttackClass):
    def __init__(self, dataset_struct, dataset_stats, model, params):
        super().__init__(dataset_struct, dataset_stats, model, params)
    
    def create_keras_classifier(self, model_stolen= None):
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        if model_stolen is None:
            original_classifier = KerasClassifier(
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
        
            return original_classifier
        else:
            stolen_classifier = KerasClassifier(
                model=model_stolen,             # The Keras model
                use_logits=False,               # Use logit outputs instead of probabilities (default: False)
                channel_index=-1,               # Index of the channel axis in the input data (default: -1)
                preprocessing_defences=None,    # Defenses for pre-processing the data (default: None)
                postprocessing_defences=None,   # Defenses for post-processing the results (default: None)
                input_layer=0,                  # Input layer of the model (default: 0)
                output_layer=-1,                # Output layer of the model (default: -1)
                channels_first=False,           # Whether channels are the first dimension in the input data (default: False)
                clip_values=(0, 1)              # Range of valid input values (default: (0,1))
                )
        
            return stolen_classifier

    def perform_attack(self, model, original_dataset, stolen_dataset):
        # Fit the original dataset
        model.fit(original_dataset[0], epochs=3, batch_size=32)

        # Wrapping the model in the ART KerasClassifier class
        classifier_original = KerasClassifier(
            model=model_original,
            clip_values=(dataset_struct["min"], dataset_struct["max"])
        )
        
        # Creating the "neural net thief" object
        # that will steal the original classifier
        copycat_cnn = CopycatCNN(
            classifier=classifier_original,     # A victim classifier
            batch_size_fit=256,                 # Size of batches for fitting the thieved classifier (default: 1)
            batch_size_query=256,               # Size of batches for querying the victim classifier (default: 1)
            nb_epochs=3,                        # Number of epochs to use for training (default: 10)
            nb_stolen=len(stolen_dataset[0]),   # Number of queries submitted to the victim classifier to steal it (default: 1)
            use_probability=False               # Use probability (default: False)
        )
        
        # Creating a reference model for theft
        model_stolen = create_keras_classifier(mdl.create_model(dataset_stats["image_shape"]), dataset_stats["num_classes"])
                                               
        # Extracting a thieved classifier
        # by training the reference model
        classifier_stolen = copycat_cnn.extract(
            x=stolen_dataset[0],                # An array with the source input to the victim classifier
            y=stolen_dataset[1],                # Target values (class labels) one-hot-encoded of shape (nb_samples, nb_classes) or indices of shape (nb_samples,). Not used in this attack
            thieved_classifier=model_stolen     # A classifier to be stolen, currently always trained on one-hot labels
            )
        
        return classifier_original, classifier_stolen
        
    def evaluate(self, original_classifier, stolen_classifier, x_test_adv):
        # Testing the performance of the original classifier
        score_original = original_classifier._model.evaluate(
            x=dataset_struct["test_data"][0],
            y=dataset_struct["test_data"][1]
            )

        # Testing the performance of the stolen classifier
        score_stolen = stolen_classifier._model.evaluate(
            x=dataset_struct["test_data"][0],
            y=dataset_struct["test_data"][1]
            )
        
        return scores_original, scores_stolen

    def print_stats(self, scores_clean, scores_adv):
        # Comparing test losses
        print(f"Original test loss: {scores_original[0]:.2f} "
            f"vs stolen test loss: {scores_stolen[0]:.2f}")

        # Comparing test accuracies
        print(f"Original test accuracy: {scores_original[1]:.2f} "
            f"vs stolen test accuracy: {scores_stolen[1]:.2f}")
        
    def plotting_stats(scores_clean, scores_adv):
        pass

def steal_model(percentage=0.5):
    # Check if the percentage is between 0 and 1
    if not 0 <= percentage <= 1:
        raise ValueError("Percentage must be between 0 and 1")
        
    # Calculate the number of elements corresponding to the percentage
    total_samples = dataset_stats["num_train_samples"]
    stolen_samples = total_samples * percentage
        
    # Setting aside a subset of the source dataset for the original model
    train_data =  dataset_struct["train_data"][0]
    train_label = dataset_struct["train_label"][1]
        
    x_original = train_data[:stolen_samples]
    y_original = train_label[:stolen_samples]

    # Using the rest of the source dataset for the stolen model
    x_stolen = train_data[stolen_samples:]
    y_stolen = train_label[stolen_samples:]
        
    return (x_original, y_original), (x_stolen, y_stolen)