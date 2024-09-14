import sys
import os
import numpy as np
import pandas as pd
import mne

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Common.FeatureExtractorBase import FeaturesExtractorBase
from Common.PublicData import biosignal_feature_maps, biosignal_maps, DevicesEnum, myo_sample_rate

class EMGFeaturesExtractor(FeaturesExtractorBase):
    
    def preprocess(self, data):
        # Extract data for each channel and transpose to match (n_channels, n_times) format
        preprocessed_data = [data[ch].values for ch in ['Ch1', 'Ch2', 'Ch3', 'Ch4', 'Ch5', 'Ch6', 'Ch7', 'Ch8']]
        return np.array(preprocessed_data)  # Shape will be (n_channels, n_times)

    def register_features(self, feature_names):
        for feature in feature_names:
            biosignal_feature_maps[biosignal_maps[DevicesEnum.myo.name][0]].append(feature)

    def extract_all_features(self, data):
        emg_features = []
        names = []

        # Ensure that data is in the shape (n_channels, n_times)
        data = np.array(data)
        print(f"Data shape: {data.shape}")  # Should print (n_channels, n_times)
        print(f"Data type: {data.dtype}")    # Should be a numeric type

        assert data.ndim == 2, "Data must be in the shape (n_channels, n_times)"
        
        # Create MNE RawArray with the correct number of channels
        ch_names = [f'Ch{i+1}' for i in range(data.shape[0])]
        info = mne.create_info(ch_names=ch_names, sfreq=myo_sample_rate, ch_types=['emg'] * data.shape[0])
        raw = mne.io.RawArray(data, info)
        print("RawArray created successfully.")

        # Print channel names to verify
        print("Channel names:", raw.info['ch_names'])

        # Print a sample of data before filtering
        print("Sample data before filtering:", data[:, :10])  # Print first 10 samples of each channel

        try:
            # Apply band-pass filter to all channels
            raw.filter(l_freq=20., h_freq=90., fir_design='firwin', picks='all')
        except Exception as e:
            print(f"Error applying filter: {e}")


        # Print a sample of data after filtering
        filtered_data = raw.get_data()
        print("Sample data after filtering:", filtered_data[:, :10])

        # Extract features for each channel
        for i in range(data.shape[0]):
            # Extract filtered data for the current channel
            filtered_data = raw.get_data(picks=[i])
            
            # Calculate features
            features = [
                np.mean(filtered_data),
                np.std(filtered_data)
            ]
            
            emg_features.extend(features)
            names.extend([f'EMG_Ch{i+1}_Mean_Filtered', f'EMG_Ch{i+1}_Std_Filtered'])

        self.register_features(names)
        return emg_features

    def extract_features(self, data):
        preprocessed_data = self.preprocess(data)
        emg_features = self.extract_all_features(preprocessed_data)
        return np.array(emg_features).flatten().tolist()  # Ensure features are returned as a flat list

 