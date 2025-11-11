# Utils
import os
import cv2
import pickle
import random

import numpy as np

class ImageSerializer(object):
    def __init__(self, dataset_dir, image_resize=(100,100)):
        """
        Initialize the ImageSerializer class.

        Parameters:
        - dataset_dir: The directory path of the dataset.
        - image_resize: Tuple representing the desired size for resizing images.
        """
        self.dataset_dir = dataset_dir
        self.image_resize = image_resize

    def get_categories(self, path=None):
        """
        Get the categories (classes) present in the specified path.

        Parameters:
        - path: The directory path containing subdirectories for each category.

        Returns:
        - categories: A list of category names.
        """
        if path is None:
            path = self.dataset_dir
            
        categories = [category for category in os.listdir(path) if '.DS_Store' not in category]
        print("Found Categories:", categories, '\n')
        return categories

    def process_images(self, path):
        """
        Process images in the specified path, resizing them and extracting labels.

        Parameters:
        - path: The directory path containing subdirectories for each category.

        Returns:
        - x_data: Numpy array containing resized image data.
        - y_data: Numpy array containing corresponding labels.
        """
        x_data = []
        y_data = []
        image_data = []
        categories = self.get_categories(path)

        for category in categories:
            category_path = os.path.join(path, category)
            class_index = categories.index(category)

            for img in os.listdir(category_path):
                img_path = os.path.join(category_path, img)

                try:
                    image_data_temp = cv2.imread(img_path)
                    image_temp_resize = cv2.resize(image_data_temp, self.image_resize)
                    image_data.append([image_temp_resize, class_index])
                except:
                    pass

        data = np.asarray(image_data)
        random.shuffle(image_data)

        for x in data:
            x_data.append(x[0])
            y_data.append(x[1])

        x_data = np.asarray(x_data) / 255.0
        y_data = np.asarray(y_data)

        return x_data, y_data

    def pickle_image(self, train=True):
        """
        Pickle the image data and labels.

        Parameters:
        - train: Boolean indicating whether to pickle training or test data.

        Returns:
        - x_data: Numpy array containing resized image data.
        - y_data: Numpy array containing corresponding labels.
        """
        if train:
            pickle_name = "Train_Data"
            label_pickle_name = "Label_Train_Data"
            data_path = os.path.join(self.dataset_dir, pickle_name)
            label_path = os.path.join(self.dataset_dir, label_pickle_name)
        else:
            pickle_name = "Test_Data"
            label_pickle_name = "Label_Test_Data"
            data_path = os.path.join(self.dataset_dir, pickle_name)
            label_path = os.path.join(self.dataset_dir, label_pickle_name)

        try:
            x_data, y_data = self.process_images(data_path)
            
            # Write the Entire Data into a Pickle File
            pickle_out = open(data_path, 'wb')
            pickle.dump(x_data, pickle_out)
            pickle_out.close()

            # Write the Y Label Data
            pickle_out = open(label_path, 'wb')
            pickle.dump(y_data, pickle_out)
            pickle_out.close()

            print(f"Pickled {'Train' if train else 'Test'} Images Successfully")
            return x_data, y_data

        except Exception as e:
            print(f"Error processing {pickle_name}: {str(e)}")
            return None

    def load_dataset(self, train=True):
        """
        Load the dataset from pickle files or process the dataset and create pickle files.

        Parameters:
        - train: Boolean indicating whether to load training or test data.

        Returns:
        - x_data: Numpy array containing resized image data.
        - y_data: Numpy array containing corresponding labels.
        """
        if train:
            pickle_name = "Train_Data"
            label_pickle_name = "Label_Train_Data"
            data_path = os.path.join(self.dataset_dir, pickle_name)
            label_path = os.path.join(self.dataset_dir, label_pickle_name)
        else:
            pickle_name = "Test_Data"
            label_pickle_name = "Label_Test_Data"
            data_path = os.path.join(self.dataset_dir, pickle_name)
            label_path = os.path.join(self.dataset_dir, label_pickle_name)

        try:
            # Read the Data from Pickle Object
            x_temp = open(data_path, 'rb')
            x_data = pickle.load(x_temp)

            y_temp = open(label_path, 'rb')
            y_data = pickle.load(y_temp)

            print(f"Reading {'Train' if train else 'Test'} Dataset from Pickle Object")

        except Exception as e:
            print(f"Could not find {pickle_name}. Loading {'Train' if train else 'Test'} dataset and creating pickle files...")
            print(e)
            
            x_data, y_data = self.pickle_image(train)

        return x_data, y_data
