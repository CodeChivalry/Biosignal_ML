import os
import pandas as pd
from pylsl import StreamInlet, resolve_stream
import threading
import time
import queue
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Common import PublicData, pd_CSVHandler

# Define a queue for each device data stream
shimmer_queue = queue.Queue()
unicorn_queue = queue.Queue()
myo_queue = queue.Queue()


# Data processing function
def process_data(device_queue, device_name, participant_id, condition_id):
    data_buffer = []
    labels = []  # Placeholder for labels, adjust as necessary
    
    data_folder = f"{PublicData.base_dir}/{participant_id}"
    os.makedirs(data_folder, exist_ok=True)
    filename = f'{data_folder}/{device_name}_{participant_id}_{condition_id}_{time.strftime("%Y-%m-%d_%H-%M-%S")}.csv'
    pd_data_saver = pd_CSVHandler.DataSaver(filename, columns=PublicData.get_header(device_name))

    while True:
        data = device_queue.get()
        if data is None:
            break
        
        timestamp, sample = data[0], data[1:]
        data_buffer.append([timestamp] + sample)
        
        if len(data_buffer) >= PublicData.NUM_SAMPLES:  # Process every 1000 samples
            # df = pd.DataFrame(data_buffer, columns=['timestamp'] + [f'channel_{i}' for i in range(len(sample))])
            pd_data_saver.save_to_csv(data_buffer)
            
            # # Extract features and train the model (example)
            # features = extract_features(data_buffer)
            # # Train the model with the extracted features (example)
            # if len(labels) >= len(data_buffer):
            #     model = train_model(features, labels)
            
            # data_buffer = []

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
unicorn_thread = threading.Thread(target=receive_data, args=('Unicorn', unicorn_queue))
myo_thread = threading.Thread(target=receive_data, args=('myo', myo_queue))

# Create threads for data processing
participant_id = "P001"  # Example participant ID
condition_id = "C001"    # Example condition ID
shimmer_processing_thread = threading.Thread(target=process_data, args=(shimmer_queue, PublicData.DevicesEnum.Shimmer.value, participant_id, condition_id))
unicorn_processing_thread = threading.Thread(target=process_data, args=(unicorn_queue, PublicData.DevicesEnum.Unicorn.value, participant_id, condition_id))
myo_processing_thread = threading.Thread(target=process_data, args=(myo_queue, PublicData.DevicesEnum.Myo.value, participant_id, condition_id))

# Start the threads
shimmer_thread.start()
unicorn_thread.start()
myo_thread.start()
shimmer_processing_thread.start()
unicorn_processing_thread.start()
myo_processing_thread.start()

# Join the threads to the main thread
shimmer_thread.join()
unicorn_thread.join()
myo_thread.join()
shimmer_processing_thread.join()
unicorn_processing_thread.join()
myo_processing_thread.join()
