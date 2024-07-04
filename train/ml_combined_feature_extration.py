import pandas as pd
from pylsl import StreamInlet, resolve_stream
import threading
import time
import queue
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Common.PublicData import NUM_SAMPLES
from FeatureHandler.EDA.EDAFeatureExtractor import EDAFeaturesExtractor 
from FeatureHandler.PPG.PPGFeatureExtractor import PPGFeaturesExtractor 
from FeatureHandler.EEG.EEGFeatureExtractor import EEGFeaturesExtractor 
from FeatureHandler.EMG.EMGFeatureExtractor import EMGFeaturesExtractor 


# Path to the dataset folder
dataset_path = '../Dataset'

# Placeholder for combined features and labels
combined_features = []
labels = []

eda_feature_extractor = EDAFeaturesExtractor()
eeg_feature_extractor = EEGFeaturesExtractor()
emg_feature_extractor = EMGFeaturesExtractor()
ppg_feature_extractor = PPGFeaturesExtractor()

# read the data from the csv file

# extract the features from the data

# extract labels from the data

# combine the features and labels

# save the combined data to a csv file
for participant_id in os.listdir(dataset_path):
    participant_folder = os.path.join(dataset_path, participant_id)
    if os.path.isdir(participant_folder):
        # Assuming file naming convention and condition, adjust as necessary
        for file in os.listdir(participant_folder):
            if file.startswith(participant_id) and ('shimmer' in file or 'emg' in file or 'eeg' in file):
                # Read the CSV file
                data_path = os.path.join(participant_folder, file)
                data = pd.read_csv(data_path)
                
                # Preprocess the data (e.g., feature extraction)
                # This is a placeholder, replace with actual preprocessing
                features = data.mean().values  # Example: using mean as a feature
                
                combined_features.append(features)
                # Extract label from file name or content
                label = extract_label(file)  # Implement this function based on your naming convention
                labels.append(label)
