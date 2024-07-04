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
from datetime import datetime, timezone
# Define a queue for each device data stream
shimmer_queue = queue.Queue()
unicorn_queue = queue.Queue()
myo_queue = queue.Queue()
marker_queue = queue.Queue()

# Global flag to control thread execution
stop_threads = False

# Data processing function
def process_data(device_queue, device_name, participant_id, condition_id):
    global stop_threads
    data_buffer = []
    labels = []  # Placeholder for labels, adjust as necessary
    
    data_folder = f"{PublicData.base_dir}/{participant_id}"
    os.makedirs(data_folder, exist_ok=True)
    filename = f'{data_folder}/{device_name}_{participant_id}_{condition_id}_{time.strftime("%Y-%m-%d_%H-%M-%S")}.csv'
    pd_data_saver = pd_CSVHandler.DataSaver(filename, columns=PublicData.header_maps[device_name])

    while not stop_threads:
        
        if stop_threads:
            break
        data = device_queue.get()
        if data is None:
            continue
        
        timestamp, sample = data[0], data[1:]
        data_buffer.append([timestamp] + sample)
        
        if len(data_buffer) >= PublicData.NUM_SAMPLES:  # Process every 1000 samples
            pd_data_saver.save_to_csv(data_buffer)
            print(f'saved {device_name} data')
            # # Extract features and train the model (example)
            # features = extract_features(data_buffer)
            # # Train the model with the extracted features (example)
            # if len(labels) >= len(data_buffer):
            #     model = train_model(features, labels)
            
            data_buffer = [] # donot comment this out, otherwise the memory will drain out

# Data reception function for each device
def receive_data(lsl_name, device_queue):
    global stop_threads
    print(f"Looking for a {lsl_name} stream...")
    streams = resolve_stream('name', lsl_name)
    inlet = StreamInlet(streams[0])
    
    while not stop_threads:
        if stop_threads:
            break
        sample, timestamp = inlet.pull_sample()
        current_utc_time = datetime.now(timezone.utc)
        current_utc_epoch_time = current_utc_time.timestamp()
        device_queue.put([timestamp,current_utc_epoch_time] + sample)

# Create threads for data reception
shimmer_thread = threading.Thread(target=receive_data, args=('shimmer', shimmer_queue))
unicorn_thread = threading.Thread(target=receive_data, args=('unicorn', unicorn_queue))
myo_thread = threading.Thread(target=receive_data, args=('myo', myo_queue))
marker_thread = threading.Thread(target=receive_data, args=('marker', marker_queue))

# Create threads for data processing
participant_id = "P002"  # Example participant ID
condition_id = "C001"    # Example condition ID
shimmer_processing_thread = threading.Thread(target=process_data, args=(shimmer_queue, PublicData.DevicesEnum.shimmer.name, participant_id, condition_id))
unicorn_processing_thread = threading.Thread(target=process_data, args=(unicorn_queue, PublicData.DevicesEnum.unicorn.name, participant_id, condition_id))
myo_processing_thread = threading.Thread(target=process_data, args=(myo_queue, PublicData.DevicesEnum.myo.name, participant_id, condition_id))
marker_processing_thread = threading.Thread(target=process_data, args=(marker_queue, PublicData.DevicesEnum.marker.name, participant_id, condition_id))

try:
    # Start the threads
    shimmer_thread.start()
    unicorn_thread.start()
    myo_thread.start()
    shimmer_processing_thread.start()
    unicorn_processing_thread.start()
    myo_processing_thread.start()
    while True:
        time.sleep(0.1) # main thread will sleep for 0.1 seconds waiting for keyboard interrupt
except KeyboardInterrupt:
    print("Detected keyboard interrupt. Shutting down...")
    stop_threads = True
    # Join the threads to the main thread
    shimmer_thread.join()
    unicorn_thread.join()
    myo_thread.join()
    shimmer_processing_thread.join()
    unicorn_processing_thread.join()
    myo_processing_thread.join()
