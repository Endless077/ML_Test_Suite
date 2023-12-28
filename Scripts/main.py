# Import Modules
import json
import sys
import os

# Own Modules
from utils.ImageSerializer import ImageSerializer
from utils.load_dataset import *
from utils.load_model import *
from utils.model import *

def load_model(model_path):
    # Replace the following line with the actual code to load your model
    print(f"Loading model from path: {model_path}")
    # return the loaded model

def load_dataset(dataset_type, params):
    # Implement the logic to load the dataset based on dataset_typeand params
    print(f"Loading {dataset_type} dataset with parameters: {params}")
    #return the loaded dataset

def perform_attack_defense(functionality, method, model, dataset_stuct, dataset_stats):
    # Implement the logic for attack or defense based on the specified functionality and method
    print(f"Performing {functionality} with method '{method}'")

def main():
    # Check the argv
    if len(sys.argv) != 2:
        print("Usage: python main.py <json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    # Disable eager execution if it is enabled and print the corresponding message
    print("Eager execution has been disabled." if tf.executing_eagerly() and tf.compat.v1.disable_eager_execution() is None else "Eager execution was already disabled.")

    # Read JSON input from file
    with open(json_file_path, 'r') as json_file:
        input_data = json.load(json_file)

    # Extract information from the JSON
    function = input_data.get("function")                   # attack or defense
    method = input_data.get("method")                       # acronym of att/def method
    dataset_type = input_data.get("dataset_type")           # mnist, cifar10, cifar100 or personal
    
    path = input_data.get("path", {})                       # path dictionary, contatins specific files path
    
    model_params = input_data.get("model_params", {})       # some model params (default: {})
    params = input_data.get("params", {})                   # some params (default: {})
  
    # Load the model
    is_trained_model = model_params["is_trained_model"]
    default_model = model_params["default_model"]
    if(is_trained_model):
        model = load_model(path["model_path"])
    else:
        if(default_model):
            model = create_model()
        else:
            model = load_model(path["model_path"])

        fit_model(train_data, test_data, model, batch_size=model_params["batch_size"], epochs=model_params["epoch"])

    # Load the dataset
    train_data, test_data, min_, max_ = load_dataset(dataset_type, path)
    dataset_stats = get_dataset_info(dataset_type, train_data[0], test_data[0], path)
    dataset_struct = {
        "train_data": train_data,
        "test_data": test_data,
        "min": min_,
        "max": max_
    }
    
    # Perform attack or defense
    perform_attack_defense(functionality, method, model, dataset_stuct, dataset_stats)

if __name__ == "__main__":
    main()
