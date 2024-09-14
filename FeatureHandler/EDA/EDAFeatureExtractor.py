import sys
import os
import numpy as np
import pandas as pd
import mne
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Common.FeatureExtractorBase import FeaturesExtractorBase
from Common.PublicData import biosignal_feature_maps, biosignal_maps, DevicesEnum, shimmer_sample_rate
import numpy as np
import neurokit2 as nk
import pandas

class EDAFeaturesExtractor(FeaturesExtractorBase):
    def preprocess(self, data):
        # Preprocess the data, extracting the 'GSR' column
        preprocessed_data = data['GSR']  # Use 'GSR' column for EDA
        return preprocessed_data

    def register_features(self, feature_list):
        # Register the feature names to the biosignal feature map
        feature_names = ['EDA_Mean', 'EDA_Std', 'SCR_Amplitude_Mean', 'SCR_RiseTime_Mean',
                         'SCR_Recovery_Mean', 'SCR_RecoveryTime_Mean']
        for feature in feature_names:
            biosignal_feature_maps[biosignal_maps[DevicesEnum.shimmer.name][0]].append(feature)

    def extract_all_features(self, data):
        # Filter the EDA signal
        x_f = nk.signal_filter(data, sampling_rate=shimmer_sample_rate, highcut=3, method="butterworth", order=4)
        
        # Process the EDA signal
        eda_signals, eda_info = nk.eda_process(x_f, shimmer_sample_rate)
        
        # Aggregate features: mean and standard deviation for EDA
        eda_mean = np.mean(eda_signals['EDA_Clean'])
        eda_std = np.std(eda_signals['EDA_Clean'])

        # SCR-related features (amplitude, rise time, recovery)
        scr_amplitude_mean = np.mean(eda_signals['SCR_Amplitude'])
        scr_rise_time_mean = np.mean(eda_signals['SCR_RiseTime'])
        scr_recovery_mean = np.mean(eda_signals['SCR_Recovery'])
        scr_recovery_time_mean = np.mean(eda_signals['SCR_RecoveryTime'])

        # Compile all features into a single list
        feature_list = [
            eda_mean, eda_std, scr_amplitude_mean,
            scr_rise_time_mean, scr_recovery_mean, scr_recovery_time_mean
        ]

        # Register the features
        self.register_features(feature_list)

        return feature_list

    def extract_features(self, data):
        # Preprocess and extract features
        preprocessed_data = self.preprocess(data)
        eda_features = self.extract_all_features(preprocessed_data)
        return eda_features
