import sys
import os
import numpy as np
import pandas as pd
import mne
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Common.FeatureExtractorBase import FeaturesExtractorBase
from Common.PublicData import biosignal_feature_maps, biosignal_maps, DevicesEnum, unicorn_sample_rate

class EEGFeaturesExtractor(FeaturesExtractorBase):
    
    def preprocess(self, data):
        # Extract data for each EEG channel
        preprocessed_data = np.column_stack([
            data['FZ'].values,
            data['C3'].values,
            data['CZ'].values,
            data['C4'].values,
            data['PZ'].values,
            data['PO7'].values,
            data['OZ'].values,
            data['PO8'].values
        ])
        return preprocessed_data  # Shape will be (n_times, n_channels)

    def register_features(self, feature_names):
        for feature in feature_names:
            biosignal_feature_maps[biosignal_maps[DevicesEnum.unicorn.name][0]].append(feature)

    def extract_all_features(self, data):
        # Ensure data is in the shape (n_times, n_channels) for MNE
        data = np.transpose(data)  # MNE expects (n_channels, n_times)
        
        # Create MNE RawArray with the correct number of channels
        ch_names = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8']
        info = mne.create_info(ch_names=ch_names, sfreq=unicorn_sample_rate, ch_types=['eeg'] * len(ch_names))
        raw = mne.io.RawArray(data, info)
        print("RawArray created successfully.")
        
        # Apply band-pass filter to all channels
        raw.filter(l_freq=1., h_freq=50., fir_design='firwin', picks='eeg')
        
        # Extract features for each channel
        eeg_features = []
        names = []
        
        for i, ch_name in enumerate(ch_names):
            # Extract filtered data for the current channel
            filtered_data = raw.get_data(picks=[i])
            
            # Calculate features
            features = [
                np.mean(filtered_data),
                np.std(filtered_data)
            ]
            
            eeg_features.extend(features)
            names.extend([f'EEG_{ch_name}_Mean_Filtered', f'EEG_{ch_name}_Std_Filtered'])
        
        self.register_features(names)
        return eeg_features

    def extract_features(self, data):
        preprocessed_data = self.preprocess(data)
        eeg_features = self.extract_all_features(preprocessed_data)
        return np.array(eeg_features).flatten().tolist()  # Ensure features are returned as a flat list

 