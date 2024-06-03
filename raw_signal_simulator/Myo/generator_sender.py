import pandas as pd
import numpy as np
import time
from pylsl import StreamInfo, StreamOutlet

# Parameters
sampling_rate = 250  # Hz

# Read data from the CSV file
csv_file = 'P01_Myo.csv'
data = pd.read_csv(csv_file)
data.columns = data.columns.str.strip()
electrode_columns = ['Electrode 1', 'Electrode 2', 'Electrode 3', 'Electrode 4', 
                     'Electrode 5', 'Electrode 6', 'Electrode 7', 'Electrode 8']

# Verify the columns are present in the DataFrame
missing_columns = [col for col in electrode_columns if col not in data.columns]
if missing_columns:
    raise KeyError(f"Missing columns in the CSV file: {missing_columns}")

electrode_data = data[electrode_columns]

# Get the number of channels from the data
num_channels = electrode_data.shape[1]

# Create a new stream info (name, type, number of channels, sampling rate, data format, source id)
info = StreamInfo('myo', 'EMG', num_channels, sampling_rate, 'float32', 'myuid34234')

# Create an outlet to stream the data
outlet = StreamOutlet(info)

# Main loop to simulate real-time data acquisition
try:
    print("Streaming EMG data from CSV... Press Ctrl+C to stop.")
    while True:
        # Stream the data via LSL
        for i in range(0, len(electrode_data), sampling_rate):
            chunk = electrode_data.iloc[i:i+sampling_rate].values  # Get a chunk of data
            for sample in chunk:
                outlet.push_sample(sample.tolist())  # Push the sample to the LSL outlet

        # Wait for one second to simulate real-time sampling rate
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulation stopped by user.")
