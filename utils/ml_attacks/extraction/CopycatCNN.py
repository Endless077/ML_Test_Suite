# Import Modules
from art.attacks.extraction import CopycatCNN as CopycatCNN_ART

# Own Modules
from classes.AttackClass import AttackClass, ExtractionAttack
from utils.model import copy_model, compile_model

'''
Implementation of the Copycat CNN attack from Rodrigues Correia-Silva et al. (2018).

Paper link: https://arxiv.org/abs/1806.05476
'''

class CopycatCNN(ExtractionAttack):
    def __init__(self, model, dataset_struct, dataset_stats, params):
        super().__init__(model, dataset_struct, dataset_stats, params)
        
    def perform_attack(self, original_dataset, stolen_dataset):
        # Fit the original dataset
        original_model = copy_model(self.model)
        original_model = compile_model(model=original_model)
        original_model.fit(original_dataset[0], epochs=self.params["epochs"], batch_size=self.params["batch_size"])

        # Wrapping the model in the ART KerasClassifier class
        classifier_original = self.create_keras_classifier(self.model)
                
        # Creating the "neural net thief" object
        # that will steal the original classifier
        copycat_cnn = CopycatCNN_ART(
            classifier=classifier_original,                 # A victim classifier
            batch_size_fit=self.params["batch_size"],       # Size of batches for fitting the thieved classifier (default: 1)
            batch_size_query=self.params["batch_size"],     # Size of batches for querying the victim classifier (default: 1)
            nb_epochs=self.params["epochs"],                 # Number of epochs to use for training (default: 10)
            nb_stolen=len(stolen_dataset[0]),               # Number of queries submitted to the victim classifier to steal it (default: 1)
            use_probability=self.params["use_probability"]  # Use probability (default: False)
        )
        
        # Creating a reference model for theft
        stolen_model = copy_model(self.model)
        stolen_model = compile_model(model=stolen_model)
        
        # Wrapping the model in the ART KerasClassifier class
        model_stolen = self.create_keras_classifier(stolen_model)
                                               
        # Extracting a thieved classifier
        # by training the reference model
        classifier_stolen = copycat_cnn.extract(
            x=stolen_dataset[0],                # An array with the source input to the victim classifier
            y=stolen_dataset[1],                # Target values (class labels) one-hot-encoded of shape (nb_samples, nb_classes) or indices of shape (nb_samples,). Not used in this attack
            thieved_classifier=model_stolen     # A classifier to be stolen, currently always trained on one-hot labels
            )
        
        return classifier_original, classifier_stolen
        
    def evaluate(self, original_classifier, stolen_classifier):
        # Testing the performance of the original classifier
        score_original = original_classifier._model.evaluate(
            x=self.dataset_struct["test_data"][0],
            y=self.dataset_struct["test_data"][1]
            )

        # Testing the performance of the stolen classifier
        score_stolen = stolen_classifier._model.evaluate(
            x=self.dataset_struct["test_data"][0],
            y=self.dataset_struct["test_data"][1]
            )
        
        return score_original, score_stolen
        
    def plotting_stats(score_clean, score_adv):
        raise NotImplementedError
    
    def result(self, score_original, score_stolen):
        # Comparing test losses
        print(f"Original test loss: {score_original[0]:.2f} "
            f"vs stolen test loss: {score_stolen[0]:.2f}")

        # Comparing test accuracies
        print(f"Original test accuracy: {score_original[1]:.2f} "
            f"vs stolen test accuracy: {score_stolen[1]:.2f}")
        
        return {}
