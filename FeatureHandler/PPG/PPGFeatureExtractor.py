import sys
import os
import numpy as np
import pandas as pd
import neurokit2 as nk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Common.FeatureExtractorBase import FeaturesExtractorBase
from Common.PublicData import biosignal_feature_maps, biosignal_maps, DevicesEnum

class PPGFeaturesExtractor(FeaturesExtractorBase):

    def preprocess(self, data):
        # Use 'HeartRatePPG(beats/min)' column for PPG
        preprocessed_data = data['HeartRatePPG(beats/min)'].values
        return preprocessed_data

    def register_features(self, feature_names):
        for feature in feature_names:
            biosignal_feature_maps[biosignal_maps[DevicesEnum.shimmer.name][1]].append(feature)

    def extract_all_features(self, data):
        # NeuroKit expects the signal to be a 1D array
        ppg_signal = data
        
        # Process the PPG signal with NeuroKit
        ppg_data = nk.ppg_process(ppg_signal, sampling_rate=1000)  # Adjust the sampling_rate if needed

        # Unpack the results
        ppg_dataframe, ppg_metadata = ppg_data
        
        # Print the columns of the DataFrame to understand its structure
        print("Columns in ppg_dataframe:", ppg_dataframe.columns)
        
        # Extract heart rate from the 'PPG_Rate' column
        heart_rate = ppg_dataframe['PPG_Rate']

        # Extract features
        ppg_features = [
            np.mean(heart_rate),
            np.std(heart_rate)
        ]

        names = ['PPG_Mean_Heart_Rate', 'PPG_Std_Heart_Rate']
        self.register_features(names)
        
        return ppg_features

    def extract_features(self, data):
        preprocessed_data = self.preprocess(data)
        ppg_features = self.extract_all_features(preprocessed_data)
        return np.array(ppg_features).flatten().tolist()  # Ensure features are returned as a flat list
    