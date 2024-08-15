import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Common.FeatureExtractorBase import FeaturesExtractorBase
from Common.PublicData import biosignal_feature_maps, biosignal_maps, DevicesEnum, shimmer_sample_rate
import numpy as np
from biosppy.signals import eda as biosppy_eda
import neurokit2 as nk
import pandas
class EDAFeaturesExtractor(FeaturesExtractorBase):

    def preprocess(self, data):
        # Placeholder for actual preprocessing logic
        preprocessed_data = data['GSR']  # Use 'GSR' column for EDA
        return preprocessed_data

    def register_features(self, feature_df:pandas.DataFrame):
        for feature in feature_df:
            biosignal_feature_maps[biosignal_maps[DevicesEnum.shimmer.name][0]].append(feature)

    def extract_all_features(self, data):
        # eda_results = biosppy_eda.eda(signal=data, sampling_rate=shimmer_sample_rate, show=False, min_amplitude=0.01)
        # eda_features = [np.mean(eda_results.amplitudes), np.std(eda_results.amplitudes)]
        x_f = nk.signal_filter(data, sampling_rate=shimmer_sample_rate, highcut=3, method="butterworth", order=4)
        eda_features = nk.eda_process(x_f,shimmer_sample_rate)
        self.register_features(eda_features)
        
        return eda_features

    def extract_features(self, data):
        preprocessed_data = self.preprocess(data)
        eda_features = self.extract_all_features(preprocessed_data)
        return eda_features
