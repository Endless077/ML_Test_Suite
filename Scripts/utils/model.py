# Import Modules
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

# Own Modules
from classes.ImageSerializer import ImageSerializer
from utils.load_model import *

def create_model(input_shape, num_classes):
    """
    Create a dynamic model based on input shape and number of classes.

    Parameters:
    - input_shape (tuple): The shape of the input images).
    - num_classes (int): The number of classes for classification.

    Returns:
    - model (tf.keras.Model): The created model.
    """
    # Shape the model
    x_input = tf.keras.layers.Input(shape=input_shape, dtype=tf.float64)
    y_input = tf.keras.layers.Input(shape=(num_classes,), dtype=tf.int64)

    # Define one_hot function
    y_one_hot = tf.keras.layers.Lambda(lambda x: to_categorical(x, num_classes=num_classes))(y_input)

    # Setup model functions
    conv1 = tf.keras.layers.Conv2D(32, (5, 5), activation='relu', padding='same')(x_input)
    pool1 = tf.keras.layers.MaxPooling2D((2, 2), strides=2)(conv1)
    conv2 = tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding='same')(pool1)
    pool2 = tf.keras.layers.MaxPooling2D((2, 2), strides=2)(conv2)
    flatten = tf.keras.layers.Flatten()(pool2)
    fc1 = tf.keras.layers.Dense(1024, activation='relu')(flatten)
    output = tf.keras.layers.Dense(num_classes, activation='softmax')(fc1)

    # Setup input/output
    model = tf.keras.models.Model(inputs=[x_input], outputs=output, name="my_model")

    # Setup optimizer
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)

    # Compile the model
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

def restore_model(model, savers_path="./model/checkpoint/", writer_path="./model/checkpoint/logs"):
    """
    Set up the model, savers, and writer.

    Parameters:
    - model (tf.keras.Model): The TensorFlow model.
    - savers_path (str): Path for saving model checkpoints.
    - writer_path (str): Path for writing TensorBoard logs.

    Returns:
    - saver (tf.train.CheckpointManager): Checkpoint manager for saving model checkpoints.
    - writer (tf.summary.SummaryWriter): Summary writer for TensorBoard.
    """
    # Verify saver path
    if not os.path.exists(savers_path):
        os.makedirs(savers_path)
        print(f"The Directory '{savers_path}' is now created.")

    # Verify writer path
    if not os.path.exists(writer_path):
        os.makedirs(writer_path)
        print(f"The Directory '{writer_path}' is now created.")

    # Setting up the metrics and the savers
    checkpoint = tf.train.Checkpoint(model=model)
    saver = tf.train.CheckpointManager(checkpoint, savers_path, max_to_keep=3)
    writer = tf.summary.create_file_writer(writer_path)
    latest_checkpoint = saver.latest_checkpoint

    if latest_checkpoint:
        checkpoint.restore(latest_checkpoint)
        print("Model Recovered at:", latest_checkpoint)
    else:
        print("No Checkpoint Found.")

    return saver, writer

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
    train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    test_data = tf.data.Dataset.from_tensor_slices((x_test, y_test))

    # Shuffle and batch train data
    train_data = train_data.shuffle(buffer_size=len(x_train)).batch(batch_size)

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
    
    # Save the trained model
    save_model(model)
    
    # Evaluation of test data
    evaluation = model.evaluate(test_data)
    print("Test Loss: {:.4f}".format(evaluation[0]))
    print("Test Accuracy: {:.2f}%".format(evaluation[1] * 100))
