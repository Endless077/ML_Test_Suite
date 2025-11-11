# Utils
import tensorflow as tf
from art.utils import load_dataset

# ImageSerializer Class
from classes.ImageSerializer import ImageSerializer

PATH = {"dataset_path_train":"../dataset/train", "dataset_path_test":"../dataset/test"}

def load_mnist():
    """
    Load and normalize the MNIST dataset.

    Returns:
    - (x_train, y_train): Tuple containing training images and labels.
    - (x_test, y_test): Tuple containing test images and labels.
    - min_ (float): Minimum value of the dataset.
    - max_ (float): Maximum value of the dataset.
    """
    # Load the MNIST dataset using TensorFlow and normalize values
    (x_train, y_train), (x_test, y_test), min_, max_ = load_dataset('mnist')
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return (x_train, y_train), (x_test, y_test), min_, max_

def load_cifar10():
    """
    Load and normalize the CIFAR-10 dataset.

    Returns:
    - (x_train, y_train): Tuple containing training images and labels.
    - (x_test, y_test): Tuple containing test images and labels.
    - min_ (float): Minimum value of the dataset.
    - max_ (float): Maximum value of the dataset.
    """
    # Load the CIFAR-10 dataset using TensorFlow and normalize values
    (x_train, y_train), (x_test, y_test), min_, max_ = load_dataset('cifar10')
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return (x_train, y_train), (x_test, y_test), min_, max_

def load_cifar100():
    """
    Load and normalize the CIFAR-100 dataset.

    Returns:
    - (x_train, y_train): Tuple containing training images and labels.
    - (x_test, y_test): Tuple containing test images and labels.
    - min_ (float): Minimum value of the dataset.
    - max_ (float): Maximum value of the dataset.
    """
    # Load the CIFAR-100 dataset using TensorFlow and normalize values
    cifar100 = tf.keras.datasets.cifar100
    (x_train, y_train), (x_test, y_test) = cifar100.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return (x_train, y_train.flatten()), (x_test, y_test.flatten()), 0.0, 1.0

def load_personal(path=PATH):
    """
    Load a custom personal dataset using the ImageSerializer class.

    Parameters:
    - path (Dict[str, str], optional): Dictionary containing paths to training and testing datasets. Default is PATH.

    Returns:
    - (x_train, y_train): Tuple containing training images and labels.
    - (x_test, y_test): Tuple containing test images and labels.
    - min_ (float): Minimum value of the dataset.
    - max_ (float): Maximum value of the dataset.
    """
    # Load the persona user dataset using some tools
    train_serializer = ImageSerializer(path["dataset_path_train"])
    test_serializer = ImageSerializer(path["dataset_path_test"])
    
    x_train, y_train = train_serializer.load_dataset(train=True)
    x_test, y_test = test_serializer.load_dataset(train=False)
    return (x_train, y_train), (x_test, y_test), 0.0, 1.0

def get_dataset_info(x_train, x_test, dataset_type, dataset_name, path=PATH):
    """
    Retrieve information about the dataset such as shape, number of classes, and sample sizes.

    Parameters:
    - x_train (tf.Tensor): Training dataset images.
    - x_test (tf.Tensor): Testing dataset images.
    - dataset_type (str): Type of the dataset (e.g., 'mnist', 'cifar10', 'cifar100', 'personal').
    - dataset_name (str): Name of the dataset.
    - path (Dict[str, str], optional): Dictionary containing paths to custom datasets. Default is PATH.

    Returns:
    - dataset_info (Dict[str, Any]): Dictionary containing information about the dataset.
    """
    # Get information from known datasets
    if dataset_type == 'mnist':
        num_classes = 10
    elif dataset_type == 'cifar10':
        num_classes = 10
    elif dataset_type == 'cifar100':
        num_classes = 100
    elif dataset_type == 'personal':
        image_serializer = ImageSerializer(dataset_dir=path["dataset_path_train"])
        categories = image_serializer.get_categories()
        num_classes = len(categories)
    else:
        raise ValueError(f"Unsupported dataset type: {dataset_type}")
    
    if(dataset_type != 'personal'):
        dataset_name = dataset_type

    num_train_samples, height, width, channels = x_train.shape
    num_test_samples = x_test.shape[0]
    
    return {
        "dataset_type": dataset_type,
        "dataset_name": dataset_name,
        "image_shape": (height, width, channels),
        "num_train_samples": num_train_samples,
        "num_test_samples": num_test_samples,
        "num_classes": num_classes
    }
    
def get_dataset(dataset_type, path=PATH):
    """
    Load a dataset based on the specified type.

    Parameters:
    - dataset_type (str): The type of dataset to load ('mnist', 'cifar10', 'cifar100', 'personal').
    - path (Dict[str, str], optional): Dictionary containing paths to custom datasets. Default is PATH.

    Returns:
    - Dataset as a tuple containing:
      - Training images and labels.
      - Testing images and labels.
      - Minimum and maximum values of the dataset.
    """
    # Check which dataset should be loaded
    if dataset_type == 'mnist':
        return load_mnist()
    elif dataset_type == 'cifar10':
        return load_cifar10()
    elif dataset_type == 'cifar100':
        return load_cifar100()
    elif dataset_type == 'personal':
        return load_personal(path)
    else:
        raise ValueError(f"Unsupported dataset type: {dataset_type}")
