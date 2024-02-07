# Import Modules
import json
import sys

# Own Modules
from utils.classes.ImageSerializer import ImageSerializer
from utils.load_dataset import *
from utils.load_model import *
from utils.model import *

def load_model(model_path):
    # Replace the following line with the actual code to load your model
    print(f"Loading model from path: {model_path}")
    # return the loaded model

def load_dataset(dataset_type, params):
    # Implement the logic to load the dataset based on dataset_type and params
    print(f"Loading {dataset_type} dataset with parameters: {params}")
    #return the loaded dataset

def perform_attack_defense(functionality, method, model, dataset_struct, dataset_stats, params):
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
    
    path = input_data.get("path", {})                       # path dictionary, contains specific files path
    
    model_params = input_data.get("model_params", {})       # some model params (default: {})
    params = input_data.get("params", {})                   # some params (default: {})
  
    # Load the dataset
    train_data, test_data, min_, max_ = load_dataset(dataset_type, path)
    dataset_stats = get_dataset_info(dataset_type, train_data[0], test_data[0], path)
    dataset_struct = {
        "train_data": train_data,
        "test_data": test_data,
        "min": min_,
        "max": max_
    }
    
    # Load the model
    vulnerable_model_path = path["vulnerable_model_path"]
    robust_model_path = path["robust_model_path"]
    model_path = path["model_path"]
    
    default_model = model_params["default_model"]
    
    if(function.lower()=="defense"):
        if(default_model):
            vulnerable_model = create_model()
            robust_model = create_model()
        else:
            vulnerable_model = load_model(vulnerable_model_path)
            robust_model = load_model(robust_model_path)
        
        model = (vulnerable_model, robust_model)
    elif(function.lower()=="attack"):
        is_trained_model = model_params["is_trained_model"]
        
        if(is_trained_model):
            model = load_model(model_path)
        else:
            if(default_model):
                model = create_model()
            else:
                model = load_model(model_path)

            fit_model(train_data, test_data, model, batch_size=model_params["batch_size"], epochs=model_params["epochs"])
    else:
        raise ValueError("Function not allowed.")
    
    # Perform attack or defense
    perform_attack_defense(function, method, model, dataset_struct, dataset_stats, params)

if __name__ == "__main__":
    main()
