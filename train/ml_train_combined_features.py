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


# Define a queue for each device data stream
shimmer_queue = queue.Queue()
unicorn_queue = queue.Queue()
myo_queue = queue.Queue()

# Feature extraction function for Shimmer
def extract_shimmer_features(data):
    # Example: Mean of each channel (excluding timestamp)
    df = pd.DataFrame(data, columns=['timestamp'] + [f'channel_{i}' for i in range(len(data[0]) - 1)])
    features = df.mean().tolist()[1:]
    return features

# Feature extraction function for EMG
def extract_emg_features(data):
    # Example: Standard deviation of each channel (excluding timestamp)
    df = pd.DataFrame(data, columns=['timestamp'] + [f'channel_{i}' for i in range(len(data[0]) - 1)])
    features = df.std().tolist()[1:]
    return features

# Feature extraction function for EEG
def extract_eeg_features(data):
    # Example: Maximum value of each channel (excluding timestamp)
    df = pd.DataFrame(data, columns=['timestamp'] + [f'channel_{i}' for i in range(len(data[0]) - 1)])
    features = df.max().tolist()[1:]
    return features

# Data processing function
def process_data(shimmer_queue, emg_queue, eeg_queue, participant_id, condition_id):
    combined_features = []  # Combined features from all streams
    labels = []  # Placeholder for labels, adjust as necessary
    data_folder = f"data_{participant_id}_{condition_id}"
    os.makedirs(data_folder, exist_ok=True)
    
    while True:
        # Get samples from all queues
        shimmer_data = shimmer_queue.get()
        emg_data = emg_queue.get()
        eeg_data = eeg_queue.get()
        
        # Check if any queue has received a termination signal
        if shimmer_data is None or emg_data is None or eeg_data is None:
            break
        
        # Extract features from each stream
        shimmer_features = extract_shimmer_features(shimmer_data)
        emg_features = extract_emg_features(emg_data)
        eeg_features = extract_eeg_features(eeg_data)
        
        # Combine features into a single feature vector
        combined_features.append(shimmer_features + emg_features + eeg_features)
        
        # Train the model with the combined feature vector (example)
        if len(labels) >= len(combined_features):
            X_train, X_test, y_train, y_test = train_test_split(combined_features, labels, test_size=0.2, random_state=42)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f'Model accuracy: {accuracy * 100:.2f}%')
            # Reset combined_features for the next training iteration
            combined_features = []

# Data reception function for each device
def receive_data(device_type, device_queue):
    print(f"Looking for a {device_type} stream...")
    streams = resolve_stream('name', device_type)
    inlet = StreamInlet(streams[0])
    
    while True:
        sample, timestamp = inlet.pull_sample()
        device_queue.put([timestamp] + sample)

# Create threads for data reception
shimmer_thread = threading.Thread(target=receive_data, args=('ECL', shimmer_queue))
emg_thread = threading.Thread(target=receive_data, args=('myo', myo_queue))
eeg_thread = threading.Thread(target=receive_data, args=('Unicorn', unicorn_queue))

# Create thread for data processing
participant_id = "P001"  # Example participant ID
condition_id = "C001"    # Example condition ID
processing_thread = threading.Thread(target=process_data, args=(shimmer_queue, myo_queue, unicorn_queue, participant_id, condition_id))

# Start the threads
shimmer_thread.start()
emg_thread.start()
eeg_thread.start()
processing_thread.start()

# Join the threads to the main thread
shimmer_thread.join()
emg_thread.join()
eeg_thread.join()
processing_thread.join()
