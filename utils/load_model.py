# Utils
import os
import tensorflow as tf

def load_model(model_path="./model"):
    # Load the model with HDF5 (.h5) format
    try:
        loaded_model = tf.keras.models.load_model(model_path)
        print(f"Model loaded successfully from {model_path} (HDF (H5) format).")
        return loaded_model
    except Exception as e:
        print(f"Error loading model from {model_path}: {str(e)} (HDF (H5) error)")

def save_model(model, filename=None, save_path="./result/model"):
    # Save the model in HDF5 (.h5) format
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    if filename is None:
        filename = "model"

    model_path = os.path.join(save_path, filename + ".h5")
    
    model.save(model_path)
    print(f"Model saved successfully in HDF (H5) format to {model_path}")
