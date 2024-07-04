# Utils
import tensorflow as tf

# Model load/save Functions
from utils.load_model import *

LOSS = tf.keras.losses.CategoricalCrossentropy()
METRICS = ["accuracy"]

OPTIMIZER = tf.keras.optimizers.Adam()

###################################################################################################

class SummaryDict:
    def __init__(self):
        self.layers = []
        self.trainable_params = 0
        self.non_trainable_params = 0

    def __call__(self, layer):
        config = layer.get_config()
        layer_info = {
            'name': config['name'],
            'output_shape': layer.output_shape,
            'num_params': layer.count_params(),
            'trainable': layer.trainable
        }
        self.layers.append(layer_info)
        if layer.trainable:
            self.trainable_params += layer.count_params()
        else:
            self.non_trainable_params += layer.count_params()

    def capture_summary(self, layer_summary):
        pass 
    
###################################################################################################

def create_model():
    """
    Create a model fron scratch for training

    Raises:
        NotImplementedError: not implemented error.
    """
    raise NotImplementedError

def compile_model(model, default=True,
                  optimizer='rmsprop',          # Optimizer to use during training (default: rmsprop)
                  loss=None,                    # Loss function to minimize during training (default: None)
                  metrics=None,                 # List of model evaluation metrics (default: None)
                  loss_weights=None,            # Weights associated with different loss functions (default: None)
                  weighted_metrics=None,        # List of metrics that have associated weights (default: None)
                  run_eagerly=None,             # Run eager execution during training (default: None)
                  steps_per_execution=None,     # Number of steps per execution during training (default: None)
                  jit_compile=None,             # Use JIT compilation during training (default: None)
                  pss_evaluation_shards=0,      # Number of shards for PSS evaluation (default: 0)
                  ):
    """
    Compile a Keras model for training with customizable options.

    Parameters:
    - model (tf.keras.Model): The Keras model to compile.
    - default (bool): Whether to compile the model with default parameters or not (default: True).
    - optimizer (str or tf.keras.optimizers.Optimizer): Optimizer to use during training (default: 'rmsprop').
    - loss (str or tf.keras.losses.Loss): Loss function to minimize during training (default: None).
    - metrics (list): List of model evaluation metrics (default: None).
    - loss_weights (list or dict): Weights associated with different loss functions (default: None).
    - weighted_metrics (list): List of metrics that have associated weights (default: None).
    - run_eagerly (bool): Run eager execution during training (default: None).
    - steps_per_execution (int): Number of steps per execution during training (default: None).
    - jit_compile (bool): Use JIT compilation during training (default: None).
    - pss_evaluation_shards (int): Number of shards for PSS evaluation (default: 0).

    Returns:
    - model (tf.keras.Model): The compiled Keras model.
    """
    if(default):
        # Compile a default model
        model.compile(
            optimizer=OPTIMIZER,
            loss=LOSS,
            metrics=METRICS
        )
    else:
        # Compile a model with given input
        model.compile(
            optimizer=optimizer,                            # Optimizer to use during training (default: rmsprop)
            loss=loss,                                      # Loss function to minimize during training (default: None)
            metrics=metrics,                                # List of model evaluation metrics (default: None)
            loss_weights=loss_weights,                      # Weights associated with different loss functions (default: None)
            weighted_metrics=weighted_metrics,              # List of metrics that have associated weights (default: None)
            run_eagerly=run_eagerly,                        # Run eager execution during training (default: None)
            steps_per_execution=steps_per_execution,        # Number of steps per execution during training (default: None)
            jit_compile=jit_compile,                        # Use JIT compilation during training (default: None)
            pss_evaluation_shards=pss_evaluation_shards     # Number of shards for PSS evaluation (default: 0)
            #**kwargs                                       # Other optional arguments
        )
    
    # Display the model's architecture
    model.summary()

    return model

def copy_model(model):
    """
    Create a copy of a Keras model.

    Parameters:
    - model (tf.keras.Model): The Keras model to copy.

    Returns:
    - copied_model (tf.keras.Model): The copied Keras model.
    """
    return tf.keras.models.clone_model(model)

def restore_model(model, savers_path="./result"):
    """
    Set up the model, savers, and writer.

    Parameters:
    - model (tf.keras.Model): The TensorFlow model.
    - savers_path (str): Path for saving model checkpoints.

    Returns:
    - saver (tf.train.CheckpointManager): Checkpoint manager for saving model checkpoints.
    """
    # Verify saver path
    if not os.path.exists(savers_path):
        os.makedirs(savers_path)
        print(f"The Directory '{savers_path}' is now created.")

    # Setting up the metrics and the savers
    checkpoint = tf.train.Checkpoint(model=model)
    saver = tf.train.CheckpointManager(checkpoint, savers_path, max_to_keep=3)
    latest_checkpoint = saver.latest_checkpoint

    if latest_checkpoint:
        checkpoint.restore(latest_checkpoint)
        print("Model Recovered at:", latest_checkpoint)
    else:
        print("No Checkpoint Found.")

    return saver

def fit_model(train_data, test_data, model, batch_size=32, epochs=10):
    """
    Fit the TensorFlow model on the provided dataset.

    Parameters:
    - train_data (Tuple): A tuple containing the training dataset (e.g., (x_train, y_train)).
    - test_data (Tuple): A tuple containing the testing dataset (e.g., (x_test, y_test)).
    - model (tf.keras.Model): The TensorFlow model to be trained.
    - batch_size (int, optional): The batch size for training and evaluation. Default is 32.
    - epochs (int, optional): The number of training epochs. Default is 10.

    Returns:
    - evaluation (List): A list containing the evaluation results (e.g., loss and accuracy) on the test dataset.
                         The first element is the test loss, and the second element is the test accuracy.
    """
    
    # Convert Data to TensorFlow
    train = tf.data.Dataset.from_tensor_slices(train_data)
    test = tf.data.Dataset.from_tensor_slices(test_data)

    # Shuffle and batch train data
    train = train_data.shuffle(buffer_size=len(train_data[0])).batch(batch_size)

    # Batch test data
    test_data = test_data.batch(batch_size)

    # Model Fit
    model.fit(train_data, epochs=epochs, batch_size=batch_size)
    """
    model.fit(
        x=None,                     # Input data (training data)
        y=None,                     # Target data (labels)
        batch_size=None,            # Number of samples per gradient update (default is 32)
        epochs=1,                   # Number of epochs to train the model
        verbose='auto',             # Verbosity mode. 'auto' prints progress bar if log level is set to 'INFO'
        callbacks=None,             # List of callbacks to apply during training
        validation_split=0.0,       # Fraction of training data to be used as validation data
        validation_data=None,       # Data on which to evaluate loss and any model metrics at the end of each epoch
        shuffle=True,               # Whether to shuffle the training data before each epoch
        class_weight=None,          # Optional dictionary mapping class indices to a weight for the class
        sample_weight=None,         # Optional array of the same length as x, providing a weight for each training sample
        initial_epoch=0,            # Epoch at which to start training (useful for resuming a previous training run)
        steps_per_epoch=None,       # Total number of steps (batches) to complete one epoch
        validation_steps=None,      # Total number of steps (batches) to complete one validation pass
        validation_batch_size=None, # Number of samples per validation batch (default is batch_size)
        validation_freq=1,          # Only relevant if validation data is provided. Specifies how often to run validation
        max_queue_size=10,          # Maximum size of the generator queue (useful to avoid resource exhaustion)
        workers=1,                  # Number of workers to use for data loading
        use_multiprocessing=False   # Whether to use multiprocessing for data loading
    )
    """
    
    return model

def summary_model(model):
    # Create an instance of SummaryDict
    summary_dict = SummaryDict()

    # Capture the model summary
    model.summary(print_fn=summary_dict.capture_summary)

    # Now summary_dict.layers contains all the information in a dictionary
    for layer in model.layers:
        summary_dict(layer)

    # If you want the entire summary as a single dictionary:
    model_summary = {
        'layer_count': len(summary_dict.layers),
        'layers': summary_dict.layers,
        'total_params': model.count_params(),
        'trainable_params': summary_dict.trainable_params,
        'non_trainable_params': summary_dict.non_trainable_params
    }
    
    return model_summary

def evaluate_model(model, test_data):
    """
    Evaluate a Keras model on test data.

    Parameters:
    - model (tf.keras.Model): The Keras model to evaluate.
    - test_data (tf.data.Dataset): The test data to evaluate the model on.

    Returns:
    - None
    """
    # Evaluation of test data
    evaluation = model.evaluate(test_data)
    print("Test Loss: {:.4f}".format(evaluation[0]))
    print("Test Accuracy: {:.2f}%".format(evaluation[1] * 100))

###################################################################################################
