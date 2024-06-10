# Utils
import os
import tensorflow as tf
from keras.models import load_model
from keras.models import load_model as keras_load_model

def load_model(model_path = "./model.h5"):
    # Try to load the model in HDF5 (H5) format
    try:
        loaded_model = keras_load_model(model_path)
        print(f"Model loaded successfully from {model_path} (HDF5 (H5) format).")
        return loaded_model
    except Exception as h5_error:
        # If loading in HDF5 (H5) format fails, try SavedModel format
        try:
            loaded_model = tf.saved_model.load(model_path)
            print(f"Model loaded successfully from {model_path} (SavedModel format).")
            return loaded_model
        except Exception as saved_model_error:
            print(f"Error loading model from {model_path}: {str(h5_error)} (HDF5 (H5) error)")
            print(f"Error loading model from {model_path}: {str(saved_model_error)} (SavedModel error)")
            return None
        
def save_model(model, filename: None, save_path="./result/model"):
    # Save the model in both HDF5 (H5) and SavedModel formats
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    model.save(save_path.join(".h5"))       # Save in HDF5 (H5) format
    tf.saved_model.save(model, save_path)   # Save in SavedModel format
    print(f"Model saved successfully to {save_path}")
