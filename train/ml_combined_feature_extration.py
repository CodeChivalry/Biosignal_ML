import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from FeatureHandler.EDA.EDAFeatureExtractor import EDAFeaturesExtractor
from FeatureHandler.PPG.PPGFeatureExtractor import PPGFeaturesExtractor
from FeatureHandler.EEG.EEGFeatureExtractor import EEGFeaturesExtractor
from FeatureHandler.EMG.EMGFeatureExtractor import EMGFeaturesExtractor

# Initialize feature extractors
eda_feature_extractor = EDAFeaturesExtractor()
eeg_feature_extractor = EEGFeaturesExtractor()
emg_feature_extractor = EMGFeaturesExtractor()
ppg_feature_extractor = PPGFeaturesExtractor()

# List of feature keys (ensure these are in the right order)
feature_keys = [
    'eda_mean', 'eda_std', 'scr_amplitude_mean', 'scr_rise_time_mean',
    'scr_recovery_mean', 'scr_recovery_time_mean', 'PPG_Mean_Heart_Rate',
    'PPG_Std_Heart_Rate', 'EEG_1_Mean', 'EEG_1_Std', 'EEG_2_Mean', 'EEG_2_Std',
    'EEG_3_Mean', 'EEG_3_Std', 'EEG_4_Mean', 'EEG_4_Std', 'EEG_5_Mean', 'EEG_5_Std',
    'EEG_6_Mean', 'EEG_6_Std', 'EEG_7_Mean', 'EEG_7_Std', 'EEG_8_Mean', 'EEG_8_Std',
    'EMG_1_Mean', 'EMG_1_Std', 'EMG_2_Mean', 'EMG_2_Std', 'EMG_3_Mean', 'EMG_3_Std',
    'EMG_4_Mean', 'EMG_4_Std', 'EMG_5_Mean', 'EMG_5_Std', 'EMG_6_Mean', 'EMG_6_Std',
    'EMG_7_Mean', 'EMG_7_Std', 'EMG_8_Mean', 'EMG_8_Std'
]

def load_data_from_csv(file_path):
    data = pd.read_csv(file_path)
    return data

# Path to the dataset folder
dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Dataset'))

# Placeholder for combined features and labels
combined_features = []
labels = []

# Function to assign label as '0' for all files
def extract_label(file_name):
    return 0  # Assign label '0' for every file

# Loop through all the files in the dataset folder
# Initialize an empty dictionary for the current file's features
file_features = {}
for file in os.listdir(dataset_path):
    data_path = os.path.join(dataset_path, file)

    if os.path.isfile(data_path):  # Ensure it's a file
        data = load_data_from_csv(data_path)
        # Extract features based on the file type
        if file.startswith('shimmer'):
            eda_features = eda_feature_extractor.extract_features(data)
            ppg_features = ppg_feature_extractor.extract_features(data)

            # Check if the correct number of features was extracted
            if len(eda_features) == 6 and len(ppg_features) == 2:
                # Create dictionaries for EDA and PPG features
                eda_dict = dict(zip(feature_keys[:6], eda_features))
                ppg_dict = dict(zip(feature_keys[6:8], ppg_features))

                # Merge dictionaries using {**dict1, **dict2}
                file_features.update(eda_dict)
                file_features.update(ppg_dict)
            else:
                raise ValueError(f"Incorrect number of EDA or PPG features extracted from file {file}")

        elif file.startswith('myo'):
            emg_features = emg_feature_extractor.extract_features(data)

            # Debug print to verify the length and content of extracted features
            print(f"Extracted EMG features: {emg_features}")

            if len(emg_features) == 16:
                emg_dict = dict(zip(feature_keys[24:], emg_features))
                file_features.update(emg_dict)  # Use update() method for merging
            else:
                raise ValueError(f"Incorrect number of EMG features extracted from file {file}")


        elif file.startswith('unicorn'):
            eeg_features = eeg_feature_extractor.extract_features(data)

            # Ensure that the correct number of EEG features is extracted
            if len(eeg_features) == 16:
                # Create a dictionary for EEG features
                eeg_dict = dict(zip(feature_keys[8:24], eeg_features))

                # Merge EEG features into the file features dictionary
                file_features.update(eeg_dict)
            else:
                raise ValueError(f"Incorrect number of EEG features extracted from file {file}")

print(f"features:{file_features}")   
label = extract_label(file)
labels.append(label)
# Check if features and labels were collected properly
print(f"Total features collected: {len(file_features)}")
combined_features.append(file_features)
# Convert the combined features to a DataFrame
if combined_features:
    features_df = pd.DataFrame(combined_features)
    features_df['Label'] = labels  # Add the label column

    # Save combined features to CSV
    output_file = os.path.join(os.path.dirname(__file__), '..', 'combined_features.csv')
    features_df.to_csv(output_file, index=False)
    print(f"Combined features and labels saved to {output_file}")
else:
    print("No features were extracted, CSV not saved.")
