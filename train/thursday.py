import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from FeatureHandler.EDA.EDAFeatureExtractor import EDAFeaturesExtractor 
from FeatureHandler.PPG.PPGFeatureExtractor import PPGFeaturesExtractor 
from FeatureHandler.EEG.EEGFeatureExtractor import EEGFeaturesExtractor 
from FeatureHandler.EMG.EMGFeatureExtractor import EMGFeaturesExtractor

def load_data_from_csv(file_path):
    print(f"Loading data from {file_path}...")
    data = pd.read_csv(file_path)
    print(f"Data loaded. Shape: {data.shape}")
    return data

def combine_features(eda_data, emg_data, eeg_data, ppg_data):
    # Initialize feature extractors
    print("Initializing feature extractors...")
    eda_extractor = EDAFeaturesExtractor()
    emg_extractor = EMGFeaturesExtractor()
    eeg_extractor = EEGFeaturesExtractor()
    ppg_extractor = PPGFeaturesExtractor()

    # Extract features from each extractor
    print("Extracting EDA features...")
    eda_features = eda_extractor.extract_features(eda_data)
    print(f"EDA features extracted: {eda_features}")

    print("Extracting EMG features...")
    emg_features = emg_extractor.extract_features(emg_data)
    print(f"EMG features extracted: {emg_features}")

    print("Extracting EEG features...")
    eeg_features = eeg_extractor.extract_features(eeg_data)
    print(f"EEG features extracted: {eeg_features}")

    print("Extracting PPG features...")
    ppg_features = ppg_extractor.extract_features(ppg_data)
    print(f"PPG features extracted: {ppg_features}")

    # Check if EDA features is a tuple and extract lists
    if isinstance(eda_features, tuple):
        eda_data_frame = eda_features[0]
        eda_dict = eda_features[1]
        
        # Convert DataFrame to a list of feature values
        eda_features_list = eda_data_frame.values.flatten().tolist()
        print(f"EDA features list (DataFrame values): {eda_features_list[:10]}")  # Print first 10 values

        # Ensure eda_dict is a dictionary with list values
        if isinstance(eda_dict, dict):
            eda_dict_values = []
            for value in eda_dict.values():
                if isinstance(value, list):
                    eda_dict_values.extend(value)
                else:
                    print(f"Warning: EDA dictionary value {value} is not a list and will be skipped.")
            print(f"EDA dictionary values (flattened): {eda_dict_values[:10]}")  # Print first 10 values
            eda_features_list += eda_dict_values
        else:
            print(f"Warning: EDA dictionary is not a valid dictionary. Got: {eda_dict}")
    else:
        eda_features_list = eda_features
        print(f"EDA features list: {eda_features_list[:10]}")  # Print first 10 values

    # Combine all features into a single list
    all_features = eda_features_list + emg_features + eeg_features + ppg_features
    print(f"Combined features length: {len(all_features)}")
    
    return all_features

# Paths to the CSV files
emg_csv_file_path = os.path.join('Dataset', 'myo_P002_C001_2024-07-23_22-54-06.csv')
eda_ppg_csv_file_path = os.path.join('Dataset', 'shimmer_P002_C001_2024-07-23_22-54-06.csv')
eeg_csv_file_path = os.path.join('Dataset', 'unicorn_P002_C001_2024-07-23_22-54-06.csv')

# Load the sample data from the CSV files
emg_data = load_data_from_csv(emg_csv_file_path)
eda_data = load_data_from_csv(eda_ppg_csv_file_path)
eeg_data = load_data_from_csv(eeg_csv_file_path)

# Extract PPG data from the same file as EDA
ppg_data = eda_data  # Assuming PPG data is in the same CSV as EDA

# Combine features
combined_features = combine_features(eda_data, emg_data, eeg_data, ppg_data)

# Print the combined feature vector
print("Combined Feature Vector:")
print(combined_features)
