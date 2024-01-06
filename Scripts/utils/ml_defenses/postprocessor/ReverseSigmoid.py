# Import Modules
from art.attacks.extraction import CopycatCNN
from art.defences.postprocessor import ReverseSigmoid
from art.estimators.classification import KerasClassifier
from art.estimators.classification import CLASSIFIER_LOSS_GRADIENTS_TYPE

# Own Modules
from utils.model import create_model
from classes.DefenseClass import DefenseClass
from ml_attacks.extraction.CopycatCNN import CopycatCNN

'''
Implementation of a postprocessor based on adding the Reverse Sigmoid perturbation to classifier output.
'''

class ReverseSigmoid(DefenseClass):
    def __init__(self, vulnerable_model, robust_model, dataset_struct, dataset_stats, params):
        super().__init__(vulnerable_model, robust_model, dataset_struct, dataset_stats, params)

    def create_keras_classifier(self, model, preprocessing_defences=None, postprocessing_defences=None):
        # Creating a classifier by wrapping our TF model in ART's KerasClassifier class
        classifier = KerasClassifier(
            model=model,                                        # The Keras model
            use_logits=False,                                   # Use logit outputs instead of probabilities (default: False)
            channel_index=-1,                                   # Index of the channel axis in the input data (default: -1)
            preprocessing_defences=preprocessing_defences,      # Defenses for pre-processing the data (default: None)
            postprocessing_defences=postprocessing_defences,    # Defenses for post-processing the results (default: None)
            input_layer=0,                                      # Input layer of the model (default: 0)
            output_layer=-1,                                    # Output layer of the model (default: -1)
            channels_first=False,                               # Whether channels are the first dimension in the input data (default: False)
            clip_values=(0, 1)                                  # Range of valid input values (default: (0,1))
            )
        
        return classifier
    
    def victim_model_perform(self, train_images_victim, train_labels_victim):
        # Creating and training a classifier
        # with the original clean data
        epochs = self.params["model_params"]["epochs"]
        
        self.model.fit(
            x=train_images_victim,
            y=train_labels_victim,
            epochs=epochs
        )
        
        # Initializing the postprocessor
        postprocessor = ReverseSigmoid(
            beta=1.0,               # The beta parameter for the Reverse Sigmoid function (default: 1.0)
            gamma=0.2,              # The gamma parameter for the Reverse Sigmoid function (default: 0.1)
            apply_fit=False,        # If True, the defense is applied during the fit (default: False)
            apply_predict=True      # If True, the defense is applied during prediction (default: True)
        )
        
        # Creating an instance of an unprotected classifier
        unprotected_classifier = self.create_keras_classifier(self.model)
        
        # Creating an instance of a protected classifier
        protected_classifier = self.create_keras_classifier(model=self.model, postprocessing_defences=postprocessor)
        
        return unprotected_classifier, protected_classifier
    
    def stolen_model_perform(self, unprotected_classifier, protected_classifier, train_images_stolen, train_labels_stolen, probabilistic=False):
        # Initializing the models that will be trained by the model extractor
        model_stolen_unprotected = KerasClassifier(model=create_model(self.dataset_stats["image_shape"], self.dataset_stats["num_classes"]), clip_values=(min, max))
        model_stolen_protected = KerasClassifier(model=create_model(self.dataset_stats["image_shape"], self.dataset_stats["num_classes"]), clip_values=(min, max))

        # Creating the "neural net thief" object
        # that will try to steal the unprotected classifier
        copycat_cnn_unprotected = CopycatCNN(
            batch_size_fit=256,
            batch_size_query=256,
            nb_epochs=3,
            nb_stolen=len(train_images_stolen),
            use_probability=probabilistic,
            classifier=unprotected_classifier
            )

        # Creating the "neural net thief" object
        # that will try to steal the protected classifier
        copycat_cnn_protected = CopycatCNN(
            batch_size_fit=256,
            batch_size_query=256,
            nb_epochs=3,
            nb_stolen=len(train_images_stolen),
            use_probability=probabilistic,
            classifier=protected_classifier
            )
        
        if(probabilistic):
            # Extracting the unprotected model
            classifier_stolen_unprotected = copycat_cnn_unprotected.extract(
                x=train_images_stolen,
                y=train_labels_stolen,
                thieved_classifier=model_stolen_unprotected
                )
            
            # Extracting the protected model
            classifier_stolen_protected = copycat_cnn_protected.extract(
                x=train_images_stolen,
                y=train_labels_stolen,
                thieved_classifier=model_stolen_protected
                )
            
            return classifier_stolen_unprotected, classifier_stolen_protected

        else:
            # Extracting the unprotected classifier
            classifier_stolen_unprotected_probabilistic = copycat_cnn_unprotected_probabilistic.extract(
                x=train_images_stolen,
                y=train_labels_stolen,
                thieved_classifier=model_stolen_unprotected
                )
            
            # Extracting the protected classifier
            classifier_stolen_protected_probabilistic = copycat_cnn_protected_probabilistic.extract(
                x=train_images_stolen,
                y=train_labels_stolen,
                thieved_classifier=model_stolen_protected
                )
            
            return classifier_stolen_unprotected_probabilistic, classifier_stolen_protected_probabilistic
        
    def perform_defense(self):
        
        # Initialize a  CopycatCNN attack
        copycatCNN_attack = CopycatCNN(self.model, self.dataset_struct, self.dataset_stats, self.params)
        
        # Setting aside a subset of the source dataset for the original model and using the rest of the source dataset for the stolen model
        train_victim, train_stolen =  copycatCNN.steal_model()

        train_images_victim = train_victim[0]
        train_labels_victim = train_victim[1]
        
        train_images_stolen = train_stolen[0]
        train_labels_stolen = train_stolen[1]
        
        # Perform victim model and stolen model postprocessor attack
        unprotected_classifier, protected_classifier = self.victim_model_perform(train_images_victim, train_labels_victim)
        
        classifier_stolen_unprotected, classifier_stolen_protected = self.stolen_model_perform(unprotected_classifier, protected_classifier, train_images_stolen, train_labels_stolen, probabilistic=False)
        classifier_stolen_unprotected_probabilistic, classifier_stolen_protected_probabilistic = self.stolen_model_perform(unprotected_classifier, protected_classifier, train_images_stolen, train_labels_stolen, probabilistic=True)
        
        return (unprotected_classifier, protected_classifier), (classifier_stolen_unprotected, classifier_stolen_protected), (classifier_stolen_unprotected_probabilistic, classifier_stolen_protected_probabilistic)
    
    def evaluate_prediction(self, unprotected_classifier, protected_classifier):
        # Getting predictions for the unprotected model
        unprotected_predictions = unprotected_classifier.predict(x=self.dataset_struct["test_data"][0][:10])
        
        # Getting predictions for the protected model
        protected_predictions = protected_classifier.predict(x=self.dataset_struct["test_data"][0])

        return unprotected_predictions, protected_predictions
    
    def evaluate_probabilistic(self, classifier_stolen_unprotected_probabilistic, classifier_stolen_protected_probabilistic):
        # Evaluating the performance of the victim model and the stolen models
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        score_stolen_unprotected_probabilistic = classifier_stolen_unprotected_probabilistic._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_protected_probabilistic = classifier_stolen_protected_probabilistic._model.evaluate(x=test_images_original, y=test_labels_original)
        
        return score_stolen_unprotected_probabilistic, score_stolen_protected_probabilistic

    def evaluate(self, unprotected_classifier, classifier_stolen_unprotected, classifier_stolen_protected):
        # Evaluating the performance of the victim model and the stolen models
        test_images_original = self.dataset_struct["test_data"][0]
        test_labels_original = self.dataset_struct["test_data"][1]
        
        score_victim = unprotected_classifier._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_unprotected = classifier_stolen_unprotected._model.evaluate(x=test_images_original, y=test_labels_original)
        score_stolen_protected = classifier_stolen_protected._model.evaluate(x=test_images_original, y=test_labels_original)

        return score_victim, score_stolen_unprotected, score_stolen_protected
    
    def print_stats_prediction(self, unprotected_predictions, protected_predictions):
        # Inspecting unprotected predictions
        print("----- ONE-HOT PREDICTIONS -----", "\n", unprotected_predictions, "\n")
        print("----- CLASS PREDICTIONS -----", "\n", np.argmax(a=unprotected_predictions, axis=1))
        
        # Inspecting protected predictions
        print("----- ONE-HOT PREDICTIONS -----", "\n", protected_predictions, "\n")
        print("----- CLASS PREDICTIONS -----", "\n", np.argmax(a=protected_predictions, axis=1))
    
    def print_stats_probabilistic(self, score_victim, score_stolen_unprotected, score_stolen_protected):
        # Comparing test losses
        print("------ TEST METRICS, ORIGINAL VS STOLEN MODELS ------\n\n")
        print("------ TEST LOSS ------\n")
        print(f"Original model: {score_victim[0]:.2f}\n"
            f"Stolen unprotected model: {score_stolen_unprotected[0]:.2f}\n"
            f"Stolen protected model: {score_stolen_protected[0]:.2f}\n")

        # Comparing test accuracies
        print("------ TEST ACCURACY ------\n")
        print(f"Original model: {score_victim[1]:.2f}\n"
            f"Stolen unprotected model: {score_stolen_unprotected[1]:.2f}\n"
            f"Stolen protected model: {score_stolen_protected[1]:.2f}\n")
    
    def print_stats(self, score_stolen_unprotected_probabilistic, score_stolen_protected_probabilistic):
        # Comparing test losses
        print("------ TEST METRICS, ORIGINAL VS PROBABILISTIC STOLEN MODELS ------\n\n")
        print("------ TEST LOSS ------\n")
        print(f"Original model: {score_victim[0]:.2f}\n"
            f"Stolen unprotected model: {score_stolen_unprotected_probabilistic[0]:.2f}\n"
            f"Stolen protected model: {score_stolen_protected_probabilistic[0]:.2f}\n")

        # Comparing test accuracies
        print("------ TEST ACCURACY ------\n")
        print(f"Original model: {score_victim[1]:.2f}\n"
            f"Stolen unprotected model: {score_stolen_unprotected_probabilistic[1]:.2f}\n"
            f"Stolen protected model: {score_stolen_protected_probabilistic[1]:.2f}\n")

    def plotting_stats(self):
        pass
