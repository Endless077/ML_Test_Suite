# Import Modules
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

# Own Modules
from Class import ImageSerializer

def create_model(input_shape=(100, 100, 3), num_classes=1):
    """
    Create a dynamic model based on input shape and number of classes.

    Parameters:
    - input_shape (tuple): The shape of the input images (default: (100, 100, 3)).
    - num_classes (int): The number of classes for classification (default: 10).

    Returns:
    - model (tf.keras.Model): The created model.
    """
    x_input = tf.keras.layers.Input(shape=input_shape, dtype=tf.float64)
    y_input = tf.keras.layers.Input(shape=(1,), dtype=tf.int64)

    y_one_hot = tf.keras.layers.Lambda(lambda x: to_categorical(x, num_classes=num_classes))(y_input)

    conv1 = tf.keras.layers.Conv2D(32, (5, 5), activation='relu', padding='same')(x_input)
    pool1 = tf.keras.layers.MaxPooling2D((2, 2), strides=2)(conv1)
    conv2 = tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding='same')(pool1)
    pool2 = tf.keras.layers.MaxPooling2D((2, 2), strides=2)(conv2)
    flatten = tf.keras.layers.Flatten()(pool2)
    fc1 = tf.keras.layers.Dense(1024, activation='relu')(flatten)
    output = tf.keras.layers.Dense(num_classes, activation='softmax')(fc1)

    model = tf.keras.models.Model(inputs=[x_input], outputs=output, name="my_model")

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)

    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

def setup_model_and_paths(model, savers_path, writer_path):
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

def fit_model(dataset, model, batch_size=32, epochs=10):
    """
    Fit the TensorFlow model on the provided dataset.

    Parameters:
    - dataset (Tuple): A tuple containing the training and testing datasets (e.g., (x_train, y_train, x_test, y_test)).
    - model (tf.keras.Model): The TensorFlow model to be trained.
    - batch_size (int, optional): The batch size for training and evaluation. Default is 32.
    - epochs (int, optional): The number of training epochs. Default is 10.

    Returns:
    - evaluation (List): A list containing the evaluation results (e.g., loss and accuracy) on the test dataset.
                         The first element is the test loss, and the second element is the test accuracy.
    """
    # Prepare the dataset for the training phase
    # Add logic to import dataset (should be loaded by personal or import by common)
    ################################################################################
    
    # Convert Data to TensorFlow
    train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    test_data = tf.data.Dataset.from_tensor_slices((x_test, y_test))

    # Shuffle and batch train data
    train_data = train_data.shuffle(buffer_size=len(x_train)).batch(batch_size)

    # Batch test data
    test_data = test_data.batch(batch_size)

    # Model Fit
    model.fit(train_data, epochs=epochs, batch_size=batch_size)

    # Evaluation of test data
    evaluation = model.evaluate(test_data)
    print("Test Loss: {:.4f}".format(evaluation[0]))
    print("Test Accuracy: {:.2f}%".format(evaluation[1] * 100))
    