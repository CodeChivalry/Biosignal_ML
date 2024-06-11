import pandas as pd
import numpy as np
import time
from pylsl import StreamInfo, StreamOutlet

# Parameters
sampling_rate = 250  # Hz
duration = 10  # seconds
num_samples = sampling_rate * duration

# Generate synthetic EMG signal
def generate_emg_signal(t):
    noise = np.random.normal(0, 0.1, len(t))
    muscle_activity = np.sin(2 * np.pi * 10 * t) * (np.random.rand(len(t)) > 0.98)
    return noise + muscle_activity

# Time vector for the duration of the signal
t = np.linspace(0, duration, num_samples)

# Columns for synthetic data
electrode_columns = ['Timestamp_outlet','Timestamp_inlet','Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7','Ch8']

# Generate synthetic data for each electrode
electrode_data = pd.DataFrame({col: generate_emg_signal(t) for col in electrode_columns})

# Get the number of channels from the data
num_channels = electrode_data.shape[1]

# Create a new stream info (name, type, number of channels, sampling rate, data format, source id)
info = StreamInfo('myo', 'EMG', num_channels, sampling_rate, 'float32', 'myuid34234')

# Create an outlet to stream the data
outlet = StreamOutlet(info)

# Main loop to simulate real-time data acquisition
try:
    print("Streaming synthetic EMG data... Press Ctrl+C to stop.")
    while True:
        # Stream the data via LSL
        for i in range(0, len(electrode_data), sampling_rate):
            chunk = electrode_data.iloc[i:i+sampling_rate]  # Get a chunk of data
            for index, row in chunk.iterrows():
                sample = row.values.tolist()  # Convert the row to a list of values
                sample_dict_list = [{col: row[col]} for col in electrode_columns] # List of dictionaries for logging 
                outlet.push_sample(sample)  # Push the sample to the LSL outlet
                timestamp = time.time()
        # Wait for one second to simulate real-time sampling rate
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulation stopped by user.")
