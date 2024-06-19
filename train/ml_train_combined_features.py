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

participant_id = "P001"  # Example participant ID
condition_id = "C001"    # Example condition ID

eda_feature_extractor = EDAFeaturesExtractor()
eeg_feature_extractor = EEGFeaturesExtractor()
emg_feature_extractor = EMGFeaturesExtractor()
ppg_feature_extractor = PPGFeaturesExtractor()

# read the data from the csv file

# extract the features from the data

# extract labels from the data

# combine the features and labels

# save the combined data to a csv file

# load the combined data from the csv file

# split the data into training and testing sets

# train the model with the training set

# test the model with the testing set

# evaluate the model

# save the model

# load the model

# make predictions with the model

# save the predictions to a csv file

# load the predictions from the csv file

# evaluate the predictions

# save the evaluation results to a csv file

# load the evaluation results from the csv file

# plot the evaluation results

# save the plot to a file

