# Import Modules
import json
import sys
import os
import tensorflow as tf
from art.utils import load_dataset

def load_mnist():
    # Load the MNIST dataset using TensorFlow and normalize values
    (x_train, y_train), (x_test, y_test), min_, max_ = load_dataset('mnist')
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return (x_train, y_train), (x_test, y_test), min_, max_

def load_cifar10():
    # Load the CIFAR-10 dataset using TensorFlow and normalize values
    (x_train, y_train), (x_test, y_test), min_, max_ = load_dataset('cifar10')
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return (x_train, y_train), (x_test, y_test), min_, max_

def load_cifar100():
    # Load the CIFAR-100 dataset using TensorFlow and normalize values
    cifar100 = tf.keras.datasets.cifar100
    (x_train, y_train), (x_test, y_test) = cifar100.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return (x_train, y_train.flatten()), (x_test, y_test.flatten()), 0.0, 1.0

def load_personal():
    # Add logic here to load your personal dataset using TensorFlow
    pass

def get_dataset_info(dataset_type, x_train, x_test):
    # Get information from known datasets
    if dataset_type == 'mnist':
        num_classes = 10
    elif dataset_type == 'cifar10':
        num_classes = 10
    elif dataset_type == 'cifar100':
        num_classes = 100
    elif dataset_type == 'personal':
        pass
    else:
        raise ValueError(f"Unsupported dataset type: {dataset_type}")
    
    num_train_samples, height, width = x_train.shape
    num_test_samples = x_test.shape[0]
    
    return {
        "dataset_type": dataset_type,
        "image_shape": (height, width),
        "num_train_samples": num_train_samples,
        "num_test_samples": num_test_samples,
        "num_classes": num_classes
    }
    
def load_dataset(dataset_type, params):
    # Check which dataset should be loaded
    if dataset_type == 'mnist':
        return load_mnist()
    elif dataset_type == 'cifar10':
        return load_cifar10()
    elif dataset_type == 'cifar100':
        return load_cifar100()
    elif dataset_type == 'personal':
        return load_personal(params)
    else:
        raise ValueError(f"Unsupported dataset type: {dataset_type}")
