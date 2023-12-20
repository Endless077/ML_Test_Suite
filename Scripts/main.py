# Import Modules
import json
import sys
import os

def load_model(model_path):
    # Replace the following line with the actual code to load your model
    print(f"Loading model from path: {model_path}")
    # return the loaded model

def load_dataset(dataset_type, method, params):
    # Implement the logic to load the dataset based on dataset_typeand params
    print(f"Loading {dataset_type} dataset with parameters: {params}")
    #return the loaded dataset

def perform_attack_defense(model, dataset, functionality, method):
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
    function = input_data.get("function")           #attack or defense
    method = input_data.get("method")               #acronym of att/def method
    dataset_type = input_data.get("dataset_type")   #mnist, cifar10, cifar100 or personal
    params = input_data.get("params", {})           #some params (if dataset_type is personal, return {})
  
    # Load the model
    model = load_model(params["model_path"])

    # Load the dataset
    train_data, test_data, min_, max_ = load_dataset(dataset_type, params)
    dataset_stats = get_dataset_info(dataset_type, train_data[0], test_data[0])
    dataset_struct = {
        "train_data": train_data,
        "test_data": test_data,
        "min": min_,
        "max": max_
    }
    
    # Perform attack or defense
    perform_attack_defense(functionality, method, model, dataset_stuct, dataset_stats, params)

if __name__ == "__main__":
    main()
