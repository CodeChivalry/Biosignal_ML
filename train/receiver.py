import pandas as pd
from pylsl import StreamInlet, resolve_stream
import threading
import time

def receive_shimmer_data():
    print("Looking for a Shimmer stream...")
    streams = resolve_stream('name', 'ECL')
    inlet = StreamInlet(streams[0])
    
    shimmer_data = []

    while True:
        sample, timestamp = inlet.pull_sample()
        shimmer_data.append([timestamp] + sample)
        if len(shimmer_data) >= 1000:  # Save every 1000 samples
            df = pd.DataFrame(shimmer_data, columns=['timestamp'] + [f'channel_{i}' for i in range(len(sample))])
            df.to_csv('shimmer_data.csv', mode='a', header=False, index=False)
            shimmer_data = []

def receive_unicorn_data():
    print("Looking for a Unicorn EEG stream...")
    streams = resolve_stream('name', 'Unicorn')
    inlet = StreamInlet(streams[0])
    
    unicorn_data = []

    while True:
        sample, timestamp = inlet.pull_sample()
        unicorn_data.append([timestamp] + sample)
        if len(unicorn_data) >= 1000:  # Save every 1000 samples
            df = pd.DataFrame(unicorn_data, columns=['timestamp'] + [f'channel_{i}' for i in range(len(sample))])
            df.to_csv('unicorn_data.csv', mode='a', header=False, index=False)
            unicorn_data = []

def receive_myo_data():
    print("Looking for a Myo EMG stream...")
    streams = resolve_stream('name', 'myo')
    inlet = StreamInlet(streams[0])
    
    myo_data = []

    while True:
        sample, timestamp = inlet.pull_sample()
        myo_data.append([timestamp] + sample)
        if len(myo_data) >= 1000:  # Save every 1000 samples
            df = pd.DataFrame(myo_data, columns=['timestamp'] + [f'channel_{i}' for i in range(len(sample))])
            df.to_csv('myo_data.csv', mode='a', header=False, index=False)
            myo_data = []

# Create threads for each device data stream
shimmer_thread = threading.Thread(target=receive_shimmer_data)
unicorn_thread = threading.Thread(target=receive_unicorn_data)
myo_thread = threading.Thread(target=receive_myo_data)

# Start the threads
shimmer_thread.start()
unicorn_thread.start()
myo_thread.start()

# Join the threads to the main thread
shimmer_thread.join()
unicorn_thread.join()
myo_thread.join()
