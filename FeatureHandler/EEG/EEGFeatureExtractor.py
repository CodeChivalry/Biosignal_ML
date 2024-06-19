import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Common.FeatureExtractorBase import FeaturesExtractorBase
from Common.PublicData import biosignal_feature_maps, biosignal_maps, DevicesEnum

class EEGFeaturesExtractor(FeaturesExtractorBase):
    # def __init__(self, config):
    #     # Initialize any necessary parameters or configurations here
    #     self.config = config

    def preprocess(self, data):
        # Implement preprocessing logic here
        # This could include normalization, filtering, etc.
        preprocessed_data = data  # Placeholder for actual preprocessing logic
        return preprocessed_data
    
    def register_features(self, feature_names):
        for feature in feature_names:
            biosignal_feature_maps[biosignal_maps[DevicesEnum.unicorn.name][0]].append(feature)
    
    # this class can be overridden in the future to extract more
    def extract_all_features(self, data):
        # Implement all feature extraction logic here
        
        # append feature names to the names list
        names = []
        # register the extracted feature names into PublicData.biosignal_feature_maps
        self.register_features(names)
        pass
        

    def extract_features(self, data):
        preprocessed_data = self.preprocess(data)
        
        ead_features = self.extract_all_features(preprocessed_data)
        
        return ead_features

